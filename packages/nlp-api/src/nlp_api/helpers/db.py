import logging
from dataclasses import dataclass

import asyncpg  # type: ignore
from common import stt
from pydantic import UUID4

logger = logging.getLogger(__name__)
type Conn = asyncpg.pool.PoolConnectionProxy | asyncpg.Connection


@dataclass
class Db:
    """
    Db helper (repository) for interfacing with postgres.
    A `pool` is usually shared across the entire application to maintain multiple persistent connections.
    """

    pool: asyncpg.Pool

    async def get_speech_to_text_task_result(
        self, audio_key: UUID4, *, connection: Conn
    ) -> stt.SpeechToTextResult | None:
        """
        Return task result if worker has finished.
        ## Example
        ```python
        db = Db(pool)
        async with db.pool.acquire() as conn:
            db.get_speech_to_text_task_result(audio_key, connection=conn)
        ```
        """

        query = """
            SELECT stt_tr.data FROM speech_to_text_task_result stt_tr
            WHERE
                stt_tr.audio_key = $1::uuid
                AND stt_tr.data IS NOT NULL
        """
        async with connection.transaction(readonly=True):
            row = await connection.fetchrow(query, audio_key)
        if row is None:
            return None
        data: str = row["data"]
        return stt.SpeechToTextResult.model_validate_json(data)
