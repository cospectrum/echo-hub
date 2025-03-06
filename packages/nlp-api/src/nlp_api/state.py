from dataclasses import dataclass
from common import stt
from pydantic import BaseModel


class ApiCfg(BaseModel):
    speech_to_text: stt.WhisperCfg | None = None


@dataclass
class ApiState:
    cfg: ApiCfg
    speech_to_text_model: stt.SpeechToTextModel | None = None
