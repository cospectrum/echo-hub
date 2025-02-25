import pytest
import nlp_worker
import pathlib

from .const import PACKAGE_ROOT


@pytest.mark.parametrize(
    ["cfg_path"],
    [
        (PACKAGE_ROOT / "config.json",),
    ],
)
def test_configs(cfg_path: pathlib.Path) -> None:
    assert cfg_path.exists(), f"{cfg_path=}"
    json = cfg_path.read_text()
    nlp_worker.WorkerCfg.model_validate_json(json)
