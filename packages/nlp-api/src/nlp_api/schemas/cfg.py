import pydantic
from common import stt
from pydantic import BaseModel, HttpUrl, ValidationError, model_validator


class S3Buckets(BaseModel):
    audio: str


class S3Settings(BaseModel):
    url: HttpUrl
    access_key: str
    secret_key: str
    buckets: S3Buckets


class RabbitMQExchanges(BaseModel):
    speech_to_text: str


class RabbitMQSettings(BaseModel):
    url: pydantic.AmqpDsn
    exchanges: RabbitMQExchanges


class PostgresSettings(BaseModel):
    url: pydantic.PostgresDsn


class ApiCfg(BaseModel):
    speech_to_text: stt.WhisperCfg | None = None
    rabbitmq: RabbitMQSettings | None = None
    postgres: PostgresSettings | None = None
    s3: S3Settings | None = None

    @model_validator(mode="after")
    def validate_queue_mode(self) -> "ApiCfg":
        queue_mode_settings = {
            "rabbitmq": self.rabbitmq,
            "postgres": self.postgres,
            "s3": self.s3,
        }
        if any(queue_mode_settings.values()):
            missing_names = [
                name for name, cfg in queue_mode_settings.items() if cfg is None
            ]
            if len(missing_names) > 0:
                raise ValidationError(
                    f"some queue mode settings are missing: {missing_names}"
                )
        return self
