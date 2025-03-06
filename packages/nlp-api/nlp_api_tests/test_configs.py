import pathlib

import pytest
from nlp_api.state import ApiCfg

from .const import CONFIGS_ROOT


@pytest.mark.parametrize(
    ["path"],
    [
        ("http_mode.json",),
    ],
)
def test_configs(path: str | pathlib.Path) -> None:
    path = CONFIGS_ROOT / path
    assert path.exists(), f"expected {path} to exists"
    ApiCfg.model_validate_json(path.read_bytes())
