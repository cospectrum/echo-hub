from common import asr
from pydantic import AmqpDsn, BaseModel, HttpUrl, PostgresDsn


class RabbitMQSettings(BaseModel):
    url: AmqpDsn
    exchange: str
    queue: str
    durable: bool = True


class S3Buckets(BaseModel):
    audio: str = "audio"


class S3Settings(BaseModel):
    url: HttpUrl
    access_key: str
    secret_key: str
    buckets: S3Buckets = S3Buckets()


class RotatingFileLoggerCfg(BaseModel):
    filename: str = "./logs.log"
    max_bytes: int | None = None


class LoggersCfg(BaseModel):
    rotating_file: RotatingFileLoggerCfg = RotatingFileLoggerCfg()


class PostgresCfg(BaseModel):
    url: PostgresDsn


class WorkerCfg(BaseModel):
    asr_model: asr.AsrModelCfg
    rabbitmq: RabbitMQSettings
    postgres: PostgresCfg
    s3: S3Settings
    loggers: LoggersCfg = LoggersCfg()
