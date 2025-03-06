from pydantic import UUID4, BaseModel


class SpeechToTextOptions(BaseModel):
    language: str | None = None


class Segment(BaseModel):
    text: str


class SpeechToTextResult(BaseModel):
    segments: list[Segment]
    language: str
    language_probability: float


class SpeechToTextTask(BaseModel):
    trace_id: str
    audio_key: UUID4
    options: SpeechToTextOptions | None = None
