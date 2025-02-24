import io
import asyncio
import logging

import common.asr as asr
import asr_api.dependencies as deps

from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile


logger = logging.getLogger(__name__)
router = APIRouter()

AsrModelDep = Annotated[asr.AsrModel, Depends(deps.get_asr_model)]


@router.post("/transcribe")
async def transcribe(
    model: AsrModelDep,
    audio: UploadFile,
    options: asr.TranscribeOptions | None = None,
) -> asr.TranscribeResult:
    audio_bytes = await audio.read()
    logger.info("%s", dict(audio_len=len(audio_bytes)))
    return await asyncio.to_thread(
        lambda: model.speech_to_text(io.BytesIO(audio_bytes), options)
    )
