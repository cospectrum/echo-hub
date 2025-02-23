from typing import Annotated
from uuid import uuid4
from common.asr import TranscribeResult
from common.schemas.transcribe import TranscribeOptions, TranscribeTask
from common.schemas import TaskId, TraceId
from fastapi import Depends, UploadFile

from .db import Db
from .queue import Queue
from .s3_service import S3


class QueueModeTranscriber:
    db: Db
    queue: Queue
    s3: S3

    def __init__(
        self,
        db: Annotated[Db, Depends(Db)],
        queue: Annotated[Queue, Depends(Queue)],
        s3: Annotated[S3, Depends(S3)],
    ) -> None:
        self.db = db
        self.queue = queue
        self.s3 = s3

    async def publish_task(
        self,
        audio: UploadFile,
        options: TranscribeOptions | None = None,
        *,
        trace_id: TraceId,
    ) -> TaskId:
        task_id = uuid4()
        audio_url = await self.s3.put(audio, key=str(task_id), bucket="transcribe")
        task = TranscribeTask(
            id=task_id, trace_id=trace_id, audio_url=audio_url, options=options
        )
        async with self.queue.acquire_channel() as ch:
            await self.queue.publish_task("transcribe", task, channel=ch)
        return task.id

    async def get_task_result(self, task_id: TaskId) -> TranscribeResult | None:
        async with self.db.acquire_connection() as conn:
            async with conn.transaction(readonly=True):
                return await self.db.get_task_result(task_id, connection=conn)
