import httpx
import pytest


@pytest.mark.asyncio
async def test_ping(nlp_api_client: httpx.AsyncClient) -> None:
    response = await nlp_api_client.get("/ping")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_metrics(nlp_api_client: httpx.AsyncClient) -> None:
    response = await nlp_api_client.get("/metrics")
    assert response.status_code == 200
