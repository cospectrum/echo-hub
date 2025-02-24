from fastapi import APIRouter

from .queue_mode import router as queue_mode_router
from .http_mode import router as http_mode_router

from nlp_api.schemas import config


def build_transcribe_router(cfg: config.ApiCfg) -> APIRouter:
    router = APIRouter()
    if cfg.http_mode_settings:
        router.include_router(http_mode_router)
    if cfg.queue_mode_settings:
        router.include_router(queue_mode_router)
    return router
