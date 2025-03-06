import contextlib
from collections.abc import Iterator
from contextlib import contextmanager

import boto3
import pika
import psycopg_pool
from common import stt
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType

from .cfg import WorkerCfg
from .worker import Worker

__all__ = [
    "new_worker",
    "WorkerCfg",
    "Worker",
]


@contextmanager
def new_worker(cfg: WorkerCfg) -> Iterator[Worker]:
    model = stt.SpeechToTextModel.from_whisper_cfg(cfg.speech_to_text)
    with contextlib.ExitStack() as stack:
        pg_pool_ctx = psycopg_pool.ConnectionPool(
            str(cfg.postgres.url),
            num_workers=1,
            min_size=1,
            max_size=1,
        )
        pg_pool: psycopg_pool.ConnectionPool = stack.enter_context(pg_pool_ctx)  # pyright: ignore

        s3_client = boto3.client(
            "s3",
            endpoint_url=str(cfg.s3.url),
            aws_access_key_id=cfg.s3.access_key,
            aws_secret_access_key=cfg.s3.secret_key,
        )

        pika_params = pika.URLParameters(str(cfg.rabbitmq.url))
        pika_conn = stack.enter_context(pika.BlockingConnection(pika_params))
        channel: BlockingChannel = stack.enter_context(pika_conn.channel())

        queue = cfg.rabbitmq.queue
        exchange = cfg.rabbitmq.exchange
        channel.exchange_declare(exchange=exchange, exchange_type=ExchangeType.fanout)
        channel.queue_declare(queue, durable=cfg.rabbitmq.durable)
        channel.queue_bind(queue=queue, exchange=exchange)
        yield Worker(
            model=model,
            channel=channel,
            pg_pool=pg_pool,
            s3_client=s3_client,
            cfg=cfg,
        )
