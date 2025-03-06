import logging
from dataclasses import dataclass

import aio_pika
import pydantic

logger = logging.getLogger(__name__)


@dataclass
class Queue:
    """
    Queue helper for interfacing with RabbitMQ.
    """

    conn: aio_pika.abc.AbstractConnection

    async def fanout_msg(
        self,
        exchange_name: str,
        msg: pydantic.BaseModel,
        *,
        channel: aio_pika.abc.AbstractChannel,
    ) -> None:
        """
        Publish message to fanout exchange.

        ## Example
        ```python
        queue = Queue(conn)
        async with queue.conn.channel() as ch:
            queue.fanout_msg("exchange_name", msg, channel=ch)
        ```
        """

        exchange = await channel.declare_exchange(
            exchange_name,
            type=aio_pika.ExchangeType.FANOUT,
        )
        msg_ = aio_pika.Message(msg.model_dump_json().encode())
        answer = await exchange.publish(msg_, routing_key="")
        logger.info("fanout msg: %s", {"exchange": exchange, "answer": answer})
