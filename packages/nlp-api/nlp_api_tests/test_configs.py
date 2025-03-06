import pytest
from nlp_api.state import ApiCfg

from .const import CONFIGS_ROOT


@pytest.mark.parametrize(
    ["filename"],
    [
        ("http_mode.json",),
        ("queue_mode.json",),
        ("http_and_queue_mode.json",),
    ],
)
def test_configs(filename: str) -> None:
    path = CONFIGS_ROOT / filename
    assert path.exists(), f"expected {path} to exists"
    ApiCfg.model_validate_json(path.read_bytes())
