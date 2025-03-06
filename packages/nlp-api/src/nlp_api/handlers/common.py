import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/ping")
async def ping() -> None:
    logger.info("ping")
