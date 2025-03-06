"""
Contains a `Worker` for `speech_to_text`, which is primarily a CPU-bound task.

The `Worker` retrieves `audio_key` values one by one from RabbitMQ,
fetches the corresponding audio file from S3, runs the speech_to_text model,
and saves the result to the database if the model succeeds.
"""

import io
import logging
from dataclasses import dataclass

import psycopg_pool
from common import stt
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel
from pydantic import UUID4, ValidationError

from . import types
from .cfg import WorkerCfg

logger = logging.getLogger(__name__)


@dataclass
class Worker:
    cfg: WorkerCfg
    pg_pool: psycopg_pool.ConnectionPool
    model: stt.SpeechToTextModel
    s3_client: types.S3Client
    channel: BlockingChannel

    def run(self) -> None:
        queue = self.cfg.rabbitmq.queue
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=self.on_msg)
        logger.info("starting worker: %s", {"queue": queue})
        self.channel.start_consuming()

    def on_msg(
        self,
        ch: BlockingChannel,
        method: spec.Basic.Deliver,
        properties: spec.BasicProperties,
        body: bytes,
    ) -> None:
        try:
            msg = stt.SpeechToTextTask.model_validate_json(body)
        except ValidationError as err:
            logger.error("failed to parse SpeechToText task: %s", {"err": err})
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        logger.info("received msg: %s", {"audio_key": msg.audio_key})
        try:
            self.process_msg(msg)
        except Exception as err:
            logger.error("failed to process msg: %s", {"err": err})
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("msg acknowledged")

    def process_msg(self, msg: stt.SpeechToTextTask) -> None:
        audio = self._fetch_audio_bytes(msg.audio_key)
        result = self.model.speech_to_text(io.BytesIO(audio))
        self._save_result(msg.audio_key, result)
        logger.info("result is saved")

    def _fetch_audio_bytes(self, audio_key: UUID4) -> bytes:
        obj = self.s3_client.get_object(
            Bucket=self.cfg.s3.buckets.audio, Key=str(audio_key)
        )
        blob = obj["Body"].read()
        logger.info(
            "got audio bytes from s3: %s",
            {"bytes_len": len(blob), "key": str(audio_key)},
        )
        return blob

    def _save_result(self, audio_key: UUID4, result: stt.SpeechToTextResult) -> None:
        query = """
            INSERT INTO speech_to_text_task_result (audio_key, data)
            VALUES (%s, %s::jsonb)
            ON CONFLICT DO NOTHING
        """
        jsonb = result.model_dump_json()
        with self.pg_pool.connection() as conn:
            with conn.cursor() as cur, conn.transaction():
                cur.execute(query, (audio_key, jsonb))
