from __future__ import annotations

from typing import Annotated, Any, Literal, Union
from pydantic import BaseModel, Field

from .whisper import Whisper, WhisperCfg
from .base import (
    AsrModel as AsrModel,
    TranscribeResult as TranscribeResult,
    TranscribeOptions as TranscribeOptions,
)


class WhisperTaggedCfg(BaseModel):
    type: Literal["whisper"]
    cfg: WhisperCfg


_Cfg = Annotated[Union[WhisperTaggedCfg], Field(discriminator="type")]


class AsrModelCfg(_Cfg):
    pass


def load_model(cfg: AsrModelCfg) -> AsrModel[Any]:
    match cfg:
        case WhisperTaggedCfg():
            return Whisper.from_cfg(cfg.cfg)
        case never:
            raise TypeError(type(never))
