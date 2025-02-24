import aio_pika
import logging

from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import Depends
from pydantic import BaseModel

from nlp_api import dependencies
from nlp_api.schemas.state import QueueModeState


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

    async def fanout_msg(
        self,
        exchange_name: str,
        msg: BaseModel,
        *,
        channel: Channel,
    ) -> None:
        exchange = await channel.declare_exchange(
            exchange_name,
            type=aio_pika.ExchangeType.FANOUT,
        )
        msg_ = aio_pika.Message(msg.model_dump_json().encode())
        answer = await exchange.publish(msg_, routing_key="")
        logger.info("fanout msg: %s", dict(exchange=exchange, answer=answer))
