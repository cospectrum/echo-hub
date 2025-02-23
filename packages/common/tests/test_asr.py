import pytest
from common import asr


@pytest.mark.parametrize(
    ["cfg"],
    [
        (asr.WhisperTaggedCfg(type="whisper", cfg=asr.WhisperCfg()),),
    ],
)
def test_load_model(
    cfg: asr.AsrModelCfg,
) -> None:
    asr.load_model(cfg)
