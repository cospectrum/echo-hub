import os
import pytest
import httpx
import pathlib

from typing import AsyncIterator


NLP_API_URL = os.getenv("NLP_API_URL", "http://localhost:6001")

TESTS_ROOT = pathlib.Path(__file__).parent
DATA_ROOT = TESTS_ROOT.parent / "data"


@pytest.fixture
async def nlp_api_client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url=NLP_API_URL) as client:
        yield client
