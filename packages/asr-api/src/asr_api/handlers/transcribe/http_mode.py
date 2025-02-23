import io
import common.asr as asr
import asr_api.dependencies as deps

from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile


router = APIRouter()


AsrModelDep = Annotated[asr.AsrModel, Depends(deps.get_asr_model)]


@router.post("/transcribe")
def transcribe(
    model: AsrModelDep,
    audio: UploadFile,
    options: asr.TranscribeOptions | None = None,
) -> asr.TranscribeResult:
    wave = audio.file.read()
    return model.speech_to_text(io.BytesIO(wave), options)
