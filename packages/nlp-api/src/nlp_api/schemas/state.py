import aio_pika
import asyncpg

from dataclasses import dataclass
from common import asr


@dataclass
class QueueModeState:
    pg_pool: asyncpg.Pool
    rabbitmq_connection: aio_pika.abc.AbstractConnection


@dataclass
class HttpModeState:
    asr_model: asr.AsrModel


@dataclass
class ApiState:
    http_mode_state: HttpModeState | None = None
    queue_mode_state: QueueModeState | None = None
