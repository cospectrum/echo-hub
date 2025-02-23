from __future__ import annotations

import io
import faster_whisper as fw

from dataclasses import dataclass
from typing import Literal
from pydantic import BaseModel
from enum import Enum

from .base import AsrModel, Segment, TranscribeOptions, TranscribeResult


__all__ = [
    "Whisper",
    "WhisperCfg",
]


class WhisperDevice(str, Enum):
    cpu = "cpu"
    cuda = "cuda"
    auto = "auto"


WhisperSize = Literal[
    "tiny",
    "tiny.en",
    "base",
    "base.en",
    "small",
    "small.en",
    "distil-small.en",
    "medium",
    "medium.en",
    "distil-medium.en",
    "large-v1",
    "large-v2",
    "large-v3",
    "large",
    "distil-large-v2",
    "distil-large-v3",
    "large-v3-turbo",
    "turbo",
]


class WhisperCfg(BaseModel):
    model_path: str | None = None
    model_size: WhisperSize = "tiny"
    device: WhisperDevice = WhisperDevice.auto


@dataclass
class Whisper(AsrModel[WhisperCfg]):
    inner: fw.WhisperModel

    @classmethod
    def from_cfg(cls, cfg: WhisperCfg) -> "Whisper":
        return cls(
            inner=fw.WhisperModel(
                cfg.model_path or cfg.model_size,
                device=cfg.device,
            )
        )

    def speech_to_text(
        self, audio: io.BytesIO, options: TranscribeOptions | None = None
    ) -> TranscribeResult:
        options = options or TranscribeOptions.default()
        whisper_segments, info = self.inner.transcribe(
            audio,
            language=options.language,
        )
        segments = []
        for whisper_segment in whisper_segments:
            segments.append(Segment(text=whisper_segment.text))
        return TranscribeResult(
            segments=segments,
            language=info.language,
            language_probability=info.language_probability,
        )
