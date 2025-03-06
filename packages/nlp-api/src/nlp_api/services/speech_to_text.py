import asyncio

from common import stt
from fastapi import Depends, UploadFile
from nlp_api import dependencies as deps
from nlp_api.state import ApiState


class SpeechToTextService:
    _model: stt.SpeechToTextModel | None

    def __init__(self, state: ApiState = Depends(deps.get_api_state)) -> None:
        self._model = state.speech_to_text_model

    async def speech_to_text(self, audio_file: UploadFile) -> stt.SpeechToTextResult:
        return await asyncio.to_thread(
            lambda: self.model.speech_to_text(audio_file.file)
        )

    @property
    def model(self) -> stt.SpeechToTextModel:
        if self._model is None:
            raise TypeError("speech to text model is not configured")
        return self._model
