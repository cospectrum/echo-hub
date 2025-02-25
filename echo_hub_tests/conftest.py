import pytest
import httpx

from typing import AsyncIterator

from .const import NLP_API_URL


@pytest.fixture
async def nlp_api_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url=NLP_API_URL) as client:
        yield client
