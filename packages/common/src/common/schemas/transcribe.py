from pydantic import UUID4, BaseModel


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


class TranscribeTask(BaseModel):
    trace_id: str
    audio_key: UUID4
    options: TranscribeOptions | None = None
