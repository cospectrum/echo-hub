import pydantic

from pydantic import BaseModel, HttpUrl, ValidationError, model_validator
from typing_extensions import Self

from common import asr


class S3Buckets(BaseModel):
    audio: str = "audio"


class S3Settings(BaseModel):
    url: HttpUrl
    access_key: str
    secret_key: str
    buckets: S3Buckets = S3Buckets()


class RabbitMQExchanges(BaseModel):
    transcribe: str = "transcribe"


class RabbitMQSettings(BaseModel):
    url: pydantic.AmqpDsn
    exchanges: RabbitMQExchanges = RabbitMQExchanges()


class PostgresSettings(BaseModel):
    url: pydantic.PostgresDsn


class QueueModeSettings(BaseModel):
    rabbitmq: RabbitMQSettings
    postgres: PostgresSettings
    s3: S3Settings


class HttpModeSettings(BaseModel):
    asr_model: asr.AsrModelCfg


class RotatingFileLoggerCfg(BaseModel):
    filename: str = "./logs.log"
    max_bytes: int | None = None


class LoggersCfg(BaseModel):
    rotating_file: RotatingFileLoggerCfg = RotatingFileLoggerCfg()


class ApiCfg(BaseModel):
    loggers: LoggersCfg = LoggersCfg()
    queue_mode_settings: QueueModeSettings | None = None
    http_mode_settings: HttpModeSettings | None = None

    @model_validator(mode="after")
    def validate_mode(self) -> Self:
        match (self.http_mode_settings, self.queue_mode_settings):
            case (None, None):
                raise ValidationError(
                    '"queue_mode_settings" and "http_mode_settings" are both missing'
                )
            case _:
                pass
        return self
