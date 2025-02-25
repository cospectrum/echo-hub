import nlp_worker
from pathlib import Path

from pydantic_settings import BaseSettings
from nlp_worker.config import configure_logging


class Settings(BaseSettings):
    cfg_path: str = "./config.json"


def main() -> None:
    settings = Settings()
    cfg = nlp_worker.WorkerCfg.model_validate_json(Path(settings.cfg_path).read_text())
    configure_logging(cfg)

    with nlp_worker.new_worker(cfg) as worker:
        worker.run()


if __name__ == "__main__":
    main()
