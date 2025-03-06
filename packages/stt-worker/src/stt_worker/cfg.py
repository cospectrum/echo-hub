from common import stt
from pydantic import AmqpDsn, BaseModel, HttpUrl, PostgresDsn


class PostgresCfg(BaseModel):
    url: PostgresDsn


class RabbitMQSettings(BaseModel):
    url: AmqpDsn
    exchange: str
    queue: str
    durable: bool = True


class S3Buckets(BaseModel):
    audio: str


class S3Settings(BaseModel):
    url: HttpUrl
    access_key: str
    secret_key: str
    buckets: S3Buckets


class WorkerCfg(BaseModel):
    speech_to_text: stt.WhisperCfg
    rabbitmq: RabbitMQSettings
    postgres: PostgresCfg
    s3: S3Settings
