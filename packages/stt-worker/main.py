from pathlib import Path

import stt_worker
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cfg_path: str = "./config.json"


def main() -> None:
    settings = Settings()
    cfg = stt_worker.WorkerCfg.model_validate_json(Path(settings.cfg_path).read_text())
    with stt_worker.new_worker(cfg) as worker:
        worker.run()


if __name__ == "__main__":
    main()
