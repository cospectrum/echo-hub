import contextlib
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import aio_pika
import aioboto3  # type: ignore
import asyncpg  # type: ignore
from common import stt
from fastapi import APIRouter, FastAPI
from pydantic_settings import BaseSettings

from nlp_api import handlers, helpers, types
from nlp_api.state import ApiCfg, ApiState

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    cfg_path: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()  # pyright: ignore[reportCallIssue]
    cfg = ApiCfg.model_validate_json(Path(settings.cfg_path).read_bytes())
    async with build_state(cfg) as state:
        app.state.api_state = state
        app.include_router(build_routes(state))
        yield


def build_routes(state: ApiState) -> APIRouter:
    router = APIRouter()
    router.include_router(handlers.common.router)
    if state.speech_to_text_model:
        router.include_router(handlers.speech_to_text.router)
    if state.supports_queue_mode():
        router.include_router(handlers.speech_to_text_task.router)
    return router


@asynccontextmanager
async def build_state(cfg: ApiCfg) -> AsyncIterator[ApiState]:
    speech_to_text_model = None
    if cfg.speech_to_text:
        speech_to_text_model = stt.SpeechToTextModel.from_whisper_cfg(
            cfg.speech_to_text
        )

    async with contextlib.AsyncExitStack() as stack:
        db, queue, s3 = (None, None, None)
        if all([cfg.postgres, cfg.rabbitmq, cfg.s3]):
            assert cfg.postgres
            assert cfg.rabbitmq
            assert cfg.s3

            pg_pool = await stack.enter_async_context(
                asyncpg.create_pool(str(cfg.postgres.url))
            )
            db = helpers.Db(pg_pool)

            rabbitmq_connection_ctx = await aio_pika.connect_robust(
                str(cfg.rabbitmq.url)
            )
            rabbitmq_connection = await stack.enter_async_context(
                rabbitmq_connection_ctx
            )
            queue = helpers.Queue(rabbitmq_connection)

            s3_session = aioboto3.Session(
                aws_access_key_id=cfg.s3.access_key,
                aws_secret_access_key=cfg.s3.secret_key,
            )
            s3_client_ctx = s3_session.client("s3", endpoint_url=str(cfg.s3.url))
            s3_client: types.S3Client = await stack.enter_async_context(s3_client_ctx)  # pyright: ignore
            s3 = helpers.S3(s3_client)
            buckets = [cfg.s3.buckets.audio]
            for bucket in buckets:
                try:
                    await s3.create_bucket(bucket)
                except Exception as err:
                    logger.warning(
                        "failed to create buckek: %s", {"err": err, "bucket": bucket}
                    )

        yield ApiState(
            cfg=cfg,
            speech_to_text_model=speech_to_text_model,
            db=db,
            queue=queue,
            s3=s3,
        )
