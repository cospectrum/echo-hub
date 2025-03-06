import io
from dataclasses import dataclass

import faster_whisper as fw

from .schemas import Segment, SpeechToTextOptions, SpeechToTextResult
from .whisper_schemas import WhisperCfg


@dataclass
class SpeechToTextModel:
    _inner: fw.WhisperModel

    def speech_to_text(
        self, audio: io.BytesIO, options: SpeechToTextOptions | None = None
    ) -> SpeechToTextResult:
        options = options or SpeechToTextOptions()
        whisper_segments, info = self._inner.transcribe(
            audio,
            language=options.language,
        )
        segments = []
        for whisper_segment in whisper_segments:
            segments.append(Segment(text=whisper_segment.text))
        return SpeechToTextResult(
            segments=segments,
            language=info.language,
            language_probability=info.language_probability,
        )

    @classmethod
    def from_whisper_cfg(cls, cfg: WhisperCfg) -> "SpeechToTextModel":
        return cls(
            _inner=fw.WhisperModel(
                cfg.model_path or cfg.model_size,
                device=cfg.device,
            )
        )
