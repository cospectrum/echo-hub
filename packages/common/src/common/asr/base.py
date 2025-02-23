from __future__ import annotations
import abc
import io

from typing import Generic, TypeVar

from common.schemas.transcribe import (
    TranscribeOptions,
    TranscribeResult,
    Segment as Segment,
)


Cfg = TypeVar("Cfg")


class AsrModel(abc.ABC, Generic[Cfg]):
    @abc.abstractmethod
    def speech_to_text(
        self, audio: io.BytesIO, options: TranscribeOptions | None = None
    ) -> TranscribeResult: ...

    @classmethod
    @abc.abstractmethod
    def from_cfg(cls, cfg: Cfg) -> AsrModel[Cfg]: ...
