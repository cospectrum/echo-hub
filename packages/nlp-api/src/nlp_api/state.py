from common import stt
from pydantic import BaseModel


class ApiCfg(BaseModel):
    speech_to_text: stt.WhisperCfg | None = None


class ApiState(BaseModel):
    cfg: ApiCfg
    speech_to_text_model: stt.SpeechToTextModel | None = None
