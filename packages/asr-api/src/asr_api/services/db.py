import asyncpg

from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator, TypeAlias

from common import asr
from common.schemas.common import TaskId
from fastapi import Depends

from asr_api import dependencies as deps
from asr_api.schemas.state import QueueModeState


Conn: TypeAlias = asyncpg.pool.PoolConnectionProxy | asyncpg.Connection


class Db:
    _pool: asyncpg.Pool

    def __init__(
        self, state: Annotated[QueueModeState, Depends(deps.get_queue_mode_state)]
    ) -> None:
        self._pool = state.pg_pool

    @asynccontextmanager
    async def acquire_connection(self) -> AsyncIterator[Conn]:
        async with self._pool.acquire() as conn:
            yield conn

    async def get_task_result(
        self, task_id: TaskId, *, connection: Conn
    ) -> asr.TranscribeResult | None:
        query = """
            SELECT tt.result FROM transcribe_task tt
            WHERE tt.id = $1::uuid AND tt.result IS NOT NULL
        """
        row = await connection.fetchrow(query, task_id)
        if row is None:
            return None
        return asr.TranscribeResult.model_validate(row["result"])
