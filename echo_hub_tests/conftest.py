from collections.abc import AsyncIterator

import httpx
import pytest

from .const import NLP_API_URL


@pytest.fixture
async def nlp_api_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url=NLP_API_URL) as client:
        yield client
