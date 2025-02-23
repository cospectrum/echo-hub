from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cfg_path: str
