import logging
import uuid
from dataclasses import dataclass

from pydantic import UUID4

from nlp_api.types import Blob, S3Client

logger = logging.getLogger(__name__)

Key = UUID4


@dataclass
class S3:
    client: S3Client

    async def create_buckets(self, buckets: set[str]) -> None:
        for bucket in buckets:
            await self.client.create_bucket(Bucket=bucket)

    async def put(self, blob: Blob, *, bucket: str, key: Key | None = None) -> Key:
        key = key or uuid.uuid4()
        await self.client.put_object(Body=blob, Bucket=bucket, Key=str(key))
        logger.info("s3 put: %s", dict(key=key, bucket=bucket))
        return key
