import asyncio

from common import stt
from fastapi import Depends, UploadFile
from nlp_api import dependencies as deps
from nlp_api.state import ApiState
from pydantic import UUID4


class SpeechToTextService:
    state: ApiState

    def __init__(self, state: ApiState = Depends(deps.get_api_state)) -> None:
        self.state = state

    async def speech_to_text(self, audio_file: UploadFile) -> stt.SpeechToTextResult:
        """
        ## Invariants
        Must be called only if "http_mode" is configured.
        """
        return await asyncio.to_thread(
            lambda: self.model.speech_to_text(audio_file.file)
        )

    async def publish_speech_to_text_task(self, audio_file: UploadFile) -> UUID4:
        """
        Publish speech to text task to async worker.
        ## Invariants
        Must be called only if "queue_mode" is configured.
        """
        queue = self.state.queue
        s3 = self.state.s3
        assert queue
        assert s3

        cfg = self.state.cfg
        assert cfg.s3
        assert cfg.rabbitmq

        audio_key = await s3.put(await audio_file.read(), bucket=cfg.s3.buckets.audio)
        task = stt.SpeechToTextTask(audio_key=audio_key)
        async with queue.conn.channel() as ch:
            await queue.fanout_msg(
                cfg.rabbitmq.exchanges.speech_to_text, task, channel=ch
            )
        return audio_key

    async def get_speech_to_text_task_result(
        self, auidio_key: UUID4
    ) -> stt.SpeechToTextResult | None:
        """
        ## Invariants
        Must be called only if "queue_mode" is configured.
        """
        db = self.state.db
        assert db
        async with db.pool.acquire() as conn:
            return await db.get_speech_to_text_task_result(auidio_key, connection=conn)

    @property
    def model(self) -> stt.SpeechToTextModel:
        if self.state.speech_to_text_model is None:
            raise TypeError("speech to text model is not configured")
        return self.state.speech_to_text_model
