from enum import Enum
from typing import Literal

from pydantic import BaseModel


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
