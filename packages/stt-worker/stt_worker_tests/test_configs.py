import pytest
import stt_worker

from .const import PACKAGE_ROOT


@pytest.mark.parametrize(
    ["filename"],
    [
        ("config.json",),
    ],
)
def test_configs(filename: str) -> None:
    cfg_path = PACKAGE_ROOT / filename
    assert cfg_path.exists(), f"{cfg_path=}"
    json = cfg_path.read_text()
    stt_worker.WorkerCfg.model_validate_json(json)
