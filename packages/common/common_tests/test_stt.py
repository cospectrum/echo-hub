import pytest
from common import stt


@pytest.mark.parametrize(
    ["cfg"],
    [
        (stt.WhisperCfg(),),
    ],
)
def test_model_from_whisper_cfg(
    cfg: stt.WhisperCfg,
) -> None:
    stt.SpeechToTextModel.from_whisper_cfg(cfg)
