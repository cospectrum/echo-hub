import aio_pika
import logging

from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from common.schemas.common import BaseTask
from fastapi import Depends

from asr_api import dependencies
from asr_api.schemas.state import QueueModeState


logger = logging.getLogger(__name__)


Channel = aio_pika.abc.AbstractChannel


class Queue:
    _conn: aio_pika.abc.AbstractConnection

    def __init__(
        self,
        state: Annotated[QueueModeState, Depends(dependencies.get_queue_mode_state)],
    ) -> None:
        self._conn = state.rabbitmq_connection

    @asynccontextmanager
    async def acquire_channel(self) -> AsyncIterator[Channel]:
        async with self._conn.channel() as ch:
            yield ch

    async def publish_task(
        self,
        exchange_name: str,
        task: BaseTask,
        *,
        channel: Channel,
    ) -> None:
        exchange = await channel.declare_exchange(
            exchange_name,
            type=aio_pika.ExchangeType.FANOUT,
        )
        msg = aio_pika.Message(task.model_dump_json().encode())
        answer = await exchange.publish(msg, routing_key="")
        logger.info("publish: %s", dict(answer=answer, task_id=task.id))
