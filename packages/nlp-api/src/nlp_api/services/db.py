import asyncpg

from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator, TypeAlias

from common import asr
from fastapi import Depends
from pydantic import UUID4

from nlp_api import dependencies as deps
from nlp_api.schemas.state import QueueModeState


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

    async def get_transcribe_task_result(
        self, audio_key: UUID4, *, connection: Conn
    ) -> asr.TranscribeResult | None:
        query = """
            SELECT tt.result FROM transcribe_task tt
            WHERE tt.id = $1::uuid AND tt.result IS NOT NULL
        """
        row = await connection.fetchrow(query, audio_key)
        if row is None:
            return None
        return asr.TranscribeResult.model_validate(row["result"])
