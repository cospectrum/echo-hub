from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from common import stt
from fastapi import APIRouter, FastAPI
from pydantic_settings import BaseSettings

from nlp_api import handlers
from nlp_api.state import ApiCfg, ApiState


class Settings(BaseSettings):
    cfg_path: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()  # pyright: ignore[reportCallIssue]
    cfg = ApiCfg.model_validate_json(Path(settings.cfg_path).read_bytes())
    state = build_state(cfg)
    app.include_router(build_routes(state))
    app.state.api_state = state
    yield


def build_routes(state: ApiState) -> APIRouter:
    router = APIRouter()
    router.include_router(handlers.common.router)
    if state.speech_to_text_model:
        router.include_router(handlers.speech_to_text.router)
    return router


def build_state(cfg: ApiCfg) -> ApiState:
    speech_to_text_model = None
    if cfg.speech_to_text:
        speech_to_text_model = stt.SpeechToTextModel.from_whisper_cfg(
            cfg.speech_to_text
        )
    return ApiState(
        cfg=cfg,
        speech_to_text_model=speech_to_text_model,
    )
