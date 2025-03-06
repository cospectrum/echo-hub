from typing import Annotated

from common import stt
from fastapi import APIRouter, Depends, UploadFile

from nlp_api.services.speech_to_text import SpeechToTextService

router = APIRouter()


@router.post("/speech_to_text")
async def speech_to_text(
    audio: UploadFile,
    service: Annotated[SpeechToTextService, Depends(SpeechToTextService)],
) -> stt.SpeechToTextResult:
    return await service.speech_to_text(audio)
