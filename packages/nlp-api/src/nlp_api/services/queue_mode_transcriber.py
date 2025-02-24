from typing import Annotated

from common.asr import TranscribeResult
from common.schemas.transcribe import TranscribeOptions, TranscribeTask

from fastapi import Depends, UploadFile
from pydantic import UUID4

from nlp_api import ctx
from nlp_api import dependencies as deps
from nlp_api.schemas.config import (
    QueueModeSettings,
    RabbitMQExchanges,
    S3Buckets,
    S3Settings,
)

from .db import Db
from .queue import Queue
from .s3_service import S3


class QueueModeTranscriber:
    db: Db
    queue: Queue
    s3: S3
    s3_buckets: S3Buckets
    exchanges: RabbitMQExchanges

    def __init__(
        self,
        db: Annotated[Db, Depends(Db)],
        queue: Annotated[Queue, Depends(Queue)],
        s3: Annotated[S3, Depends(S3)],
        s3_settings: Annotated[S3Settings, Depends(deps.get_s3_settings)],
        queue_mode_settings: Annotated[
            QueueModeSettings, Depends(deps.get_queue_mode_settings)
        ],
    ) -> None:
        self.db = db
        self.queue = queue
        self.s3 = s3
        self.s3_buckets = s3_settings.buckets
        self.exchanges = queue_mode_settings.rabbitmq.exchanges

    async def post_task(
        self,
        audio: UploadFile,
        options: TranscribeOptions | None = None,
    ) -> UUID4:
        audio_key = await self.s3.put(await audio.read(), bucket=self.s3_buckets.audio)
        task = TranscribeTask(
            trace_id=ctx.trace_id.get(), audio_key=audio_key, options=options
        )
        async with self.queue.acquire_channel() as ch:
            await self.queue.fanout_msg(self.exchanges.transcribe, task, channel=ch)
        return audio_key

    async def get_task_result(self, auidio_key: UUID4) -> TranscribeResult | None:
        async with self.db.acquire_connection() as conn:
            return await self.db.get_transcribe_task_result(auidio_key, connection=conn)
