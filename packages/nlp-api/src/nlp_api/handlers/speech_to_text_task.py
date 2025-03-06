from typing import Annotated

from common import stt
from fastapi import APIRouter, Depends, UploadFile
from pydantic import UUID4

from nlp_api.services.speech_to_text import SpeechToTextService

router = APIRouter()

ServiceDep = Annotated[SpeechToTextService, Depends(SpeechToTextService)]


@router.post("/speech_to_text/task")
async def post_transcribe_task(
    service: ServiceDep,
    audio: UploadFile,
) -> UUID4:
    return await service.publish_speech_to_text_task(audio)


@router.get("/speech_to_text/task")
async def get_transcribe_task(
    service: ServiceDep, audio_key: UUID4
) -> stt.SpeechToTextResult | None:
    return await service.get_speech_to_text_task_result(audio_key)
