import contextlib
import io
import logging
import boto3
import psycopg_pool
import pika

from pika.channel import Channel as PikaChannel

from dataclasses import dataclass
from typing import Iterator
from pika.exchange_type import ExchangeType
from pydantic import UUID4

from common import asr
from common.schemas.transcribe import TranscribeTask

from . import ctx
from . import types
from .config.schema import WorkerCfg


logger = logging.getLogger(__name__)


@contextlib.contextmanager
def new_worker(cfg: WorkerCfg) -> Iterator["Worker"]:
    model = asr.load_model(cfg.asr_model)
    with contextlib.ExitStack() as stack:
        pg_pool_ctx = psycopg_pool.ConnectionPool(
            str(cfg.postgres.url),
            num_workers=1,
            min_size=1,
            max_size=1,
        )
        pg_pool: psycopg_pool.ConnectionPool = stack.enter_context(pg_pool_ctx)  # type: ignore

        s3_client = boto3.client(
            "s3",
            endpoint_url=str(cfg.s3.url),
            aws_access_key_id=cfg.s3.access_key,
            aws_secret_access_key=cfg.s3.secret_key,
        )

        pika_params = pika.URLParameters(str(cfg.rabbitmq.url))
        pika_conn = stack.enter_context(pika.BlockingConnection(pika_params))
        channel: PikaChannel = stack.enter_context(pika_conn.channel())

        queue = cfg.rabbitmq.queue
        exchange = cfg.rabbitmq.exchange
        channel.exchange_declare(exchange=exchange, exchange_type=ExchangeType.fanout)
        channel.queue_declare(queue, durable=cfg.rabbitmq.durable)
        channel.queue_bind(queue=queue, exchange=exchange)
        logger.info("declared exchange and queue", dict(queue=queue, exchange=exchange))
        yield Worker(
            model=model,
            channel=channel,
            pg_pool=pg_pool,
            s3_client=s3_client,
            cfg=cfg,
        )


@dataclass
class Worker:
    model: asr.AsrModel
    channel: PikaChannel
    pg_pool: psycopg_pool.ConnectionPool
    s3_client: types.S3Client
    cfg: WorkerCfg

    def run(self) -> None:
        queue = self.cfg.rabbitmq.queue
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=self.on_msg)
        logger.info("starting worker: %s", dict(queue=queue))
        self.channel.start_consuming()  # type: ignore

    def get_audio_bytes(self, audio_key: UUID4) -> bytes:
        obj = self.s3_client.get_object(
            Bucket=self.cfg.s3.buckets.audio, Key=str(audio_key)
        )
        blob = obj["Body"].read()
        logger.info(
            "got audio bytes from s3: %s", dict(bytes_len=len(blob), key=str(audio_key))
        )
        return blob

    def save_result(self, audio_key: UUID4, result: asr.TranscribeResult) -> None:
        query = """
            INSERT INTO transcribe_task_result (audio_key, data)
            VALUES (%s, %s::jsonb)
            ON CONFLICT DO NOTHING
        """
        jsonb = result.model_dump_json()
        with self.pg_pool.connection() as conn:
            with conn.cursor() as cur, conn.transaction():
                cur.execute(query, (audio_key, jsonb))

    def on_msg(self, ch: PikaChannel, method, properties, body: bytes) -> None:
        msg = TranscribeTask.model_validate_json(body)
        ctx.trace_id.set(msg.trace_id)
        logger.info("received msg: %s", dict(audio_key=msg.audio_key))

        audio = self.get_audio_bytes(msg.audio_key)
        result = self.model.speech_to_text(io.BytesIO(audio))
        self.save_result(msg.audio_key, result)
        logger.info("result is saved")

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("msg acknowledged")
