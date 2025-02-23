from pydantic import BaseModel, HttpUrl

from .common import BaseTask


class TranscribeOptions(BaseModel):
    language: str | None = None

    @classmethod
    def default(cls) -> "TranscribeOptions":
        return cls()


class Segment(BaseModel):
    text: str


class TranscribeResult(BaseModel):
    segments: list[Segment]
    language: str
    language_probability: float


class TranscribeTask(BaseTask):
    audio_url: HttpUrl
    options: TranscribeOptions | None = None
