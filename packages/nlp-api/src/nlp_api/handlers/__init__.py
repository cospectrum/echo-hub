from fastapi import APIRouter

from . import transcribe
from .common import router as common_router

from ..schemas import config


def build_router(cfg: config.ApiCfg) -> APIRouter:
    router = APIRouter()
    router.include_router(transcribe.build_transcribe_router(cfg))
    router.include_router(common_router)
    return router
