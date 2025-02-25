import logging
import uuid

from typing import Annotated
from fastapi import Depends
from pydantic import UUID4

from nlp_api import dependencies as deps
from nlp_api.types import S3Client, Blob


logger = logging.getLogger(__name__)


Key = UUID4


class S3:
    client: S3Client

    def __init__(
        self,
        client: Annotated[S3Client, Depends(deps.get_s3_client)],
    ) -> None:
        self.client = client

    async def put(self, blob: Blob, *, bucket: str, key: Key | None = None) -> Key:
        key = key or uuid.uuid4()
        await self.client.put_object(Body=blob, Bucket=bucket, Key=str(key))
        logger.info("s3 put: %s", dict(key=key, bucket=bucket))
        return key
