from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile

from common import asr
from pydantic import UUID4

from nlp_api.services.queue_mode_transcriber import QueueModeTranscriber


router = APIRouter()

ServiceDep = Annotated[QueueModeTranscriber, Depends(QueueModeTranscriber)]


@router.post("/transcribe/task")
async def post_transcribe_task(
    service: ServiceDep,
    audio: UploadFile,
) -> UUID4:
    return await service.post_task(audio)


@router.get("/transcribe/task")
async def get_transcribe_task(
    service: ServiceDep, audio_key: UUID4
) -> asr.TranscribeResult | None:
    return await service.get_task_result(audio_key)
