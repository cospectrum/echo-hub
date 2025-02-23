from fastapi import APIRouter

from . import transcribe

from ..schemas import config


def build_router(cfg: config.ApiCfg) -> APIRouter:
    router = APIRouter()
    router.include_router(transcribe.build_transcribe_router(cfg))
    return router
