import pytest
import uuid
import httpx

from echo_hub_tests.const import DATA_ROOT


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "filename",
    ],
    [
        ("hello_there.mp3",),
    ],
)
async def test_post_task(
    filename: str,
    nlp_api_client: httpx.AsyncClient,
) -> None:
    ROUTE = "/transcribe/task"
    audio_path = DATA_ROOT / "audio" / filename
    assert audio_path.exists(), f"expected {audio_path=} to exist"

    with open(audio_path, "rb") as file:
        files = {"audio": (file.name, file, "audio/mpeg")}
        response = await nlp_api_client.post(ROUTE, files=files)
    assert response.status_code == 200

    body = response.json()
    uuid.UUID(body)


@pytest.mark.asyncio
async def test_get_random_task(
    nlp_api_client: httpx.AsyncClient,
) -> None:
    ROUTE = "/transcribe/task"

    audio_key = uuid.uuid4()
    response = await nlp_api_client.get(ROUTE, params=dict(audio_key=str(audio_key)))
    assert response.status_code == 200
