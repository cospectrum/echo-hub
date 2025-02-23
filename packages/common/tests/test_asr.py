import pytest
from common import asr


@pytest.mark.parametrize(
    ["raw"],
    [
        ('{"type": "whisper", "cfg": {}}',),
    ],
)
def test_cfg_parsing(raw: str) -> None:
    cfg = asr.AsrModelCfg.model_validate_json(raw)
    assert cfg == asr.AsrModelCfg.model_validate(cfg.model_dump())


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
