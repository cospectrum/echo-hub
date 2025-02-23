import logging
import os
from typing import Annotated
from fastapi import Depends, UploadFile
from pydantic import HttpUrl

from asr_api.schemas.config import S3Settings
from asr_api import dependencies as deps


logger = logging.getLogger(__name__)


class S3:
    _base_url: HttpUrl

    def __init__(
        self, cfg: Annotated[S3Settings, Depends(deps.get_s3_settings)]
    ) -> None:
        self._base_url = cfg.base_url

    def _url(self, *, bucket: str, key: str) -> HttpUrl:
        path = os.path.join(str(self._base_url), bucket, key)
        return HttpUrl(path)

    async def put(self, file: UploadFile, *, key: str, bucket: str) -> HttpUrl:
        file_data = await file.read()
        url = self._url(bucket=bucket, key=key)
        logger.info("s3 put: %s", dict(url=url, file_len=len(file_data)))
        return url
