import contextlib
import pathlib
import aio_pika
import aioboto3
import asyncpg
import logging

from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI

from common import asr

from nlp_api.types import S3Client

from .env import Settings
from .log import configure_logging

from .. import handlers
from ..schemas import state as state_schemas
from ..schemas.config import (
    ApiCfg,
    HttpModeSettings,
    QueueModeSettings,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()  # pyright: ignore[reportCallIssue]
    cfg = ApiCfg.model_validate_json(pathlib.Path(settings.cfg_path).read_bytes())
    configure_logging(cfg)

    app.state.api_cfg = cfg
    api_state: state_schemas.ApiState
    async with create_api_state(cfg) as api_state:
        app.state.api_state = api_state
        app.include_router(handlers.build_router(cfg))
        logger.info("configured app")
        yield


@asynccontextmanager
async def create_api_state(cfg: ApiCfg) -> AsyncIterator[state_schemas.ApiState]:
    assert cfg.queue_mode_settings or cfg.http_mode_settings

    async with contextlib.AsyncExitStack() as stack:
        http_mode_state = None
        if cfg.http_mode_settings:
            http_mode_state = await stack.enter_async_context(
                create_http_mode_state(cfg.http_mode_settings)
            )

        queue_mode_state = None
        if cfg.queue_mode_settings:
            queue_mode_state = await stack.enter_async_context(
                create_queue_mode_state(cfg.queue_mode_settings)
            )

        assert http_mode_state or queue_mode_state
        yield state_schemas.ApiState(
            http_mode_state=http_mode_state,
            queue_mode_state=queue_mode_state,
        )


@asynccontextmanager
async def create_http_mode_state(
    cfg: HttpModeSettings,
) -> AsyncIterator[state_schemas.HttpModeState]:
    yield state_schemas.HttpModeState(
        asr_model=asr.load_model(cfg.asr_model),
    )


@asynccontextmanager
async def create_queue_mode_state(
    cfg: QueueModeSettings,
) -> AsyncIterator[state_schemas.QueueModeState]:
    async with contextlib.AsyncExitStack() as stack:
        pg_pool = await stack.enter_async_context(
            asyncpg.create_pool(str(cfg.postgres.url))
        )

        rabbitmq_connection_ctx = await aio_pika.connect_robust(str(cfg.rabbitmq.url))
        rabbitmq_connection = await stack.enter_async_context(rabbitmq_connection_ctx)

        s3_session = aioboto3.Session(
            aws_access_key_id=cfg.s3.access_key,
            aws_secret_access_key=cfg.s3.secret_key,
        )
        s3_client_ctx = s3_session.client("s3", endpoint_url=str(cfg.s3.url))
        s3_client: S3Client = await stack.enter_async_context(s3_client_ctx)  # type: ignore
        buckets = [cfg.s3.buckets.audio]
        for bucket in buckets:
            try:
                await s3_client.create_bucket(Bucket=bucket)
            except Exception as e:
                logger.warning("failed to create bucket: %s", e)

        yield state_schemas.QueueModeState(
            pg_pool=pg_pool,
            rabbitmq_connection=rabbitmq_connection,
            s3_client=s3_client,
        )
