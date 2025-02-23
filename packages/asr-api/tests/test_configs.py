import pytest
import pathlib

from asr_api.schemas import config


ROOT = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    ["path"],
    [
        ("../configs/http_mode.json",),
        ("../configs/queue_mode.json",),
        ("../configs/http_and_queue_mode.json",),
    ],
)
def test_configs(path: str | pathlib.Path) -> None:
    path = ROOT / path
    assert path.exists(), f"expected {path} to exists"
    config.ApiCfg.model_validate_json(path.read_bytes())
