from dataclasses import dataclass

from common import stt

from . import helpers
from .schemas.cfg import ApiCfg as ApiCfg


@dataclass
class ApiState:
    cfg: ApiCfg
    speech_to_text_model: stt.SpeechToTextModel | None
    db: helpers.Db | None
    queue: helpers.Queue | None
    s3: helpers.S3 | None

    def supports_queue_mode(self) -> bool:
        return all([self.db, self.queue, self.s3])
