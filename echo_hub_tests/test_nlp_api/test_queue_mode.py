import pytest
import asyncio
import uuid
import httpx

from echo_hub_tests.const import DATA_ROOT
from common import asr


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["filename", "language", "segments"],
    [
        ("hello_there.mp3", "en", ["Hello there."]),
    ],
)
async def test_transcribe_task(
    filename: str,
    language: str,
    segments: str,
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
    audio_key = uuid.UUID(body)
    result = None
    for _ in range(30):
        await asyncio.sleep(1)
        response = await nlp_api_client.get(
            ROUTE, params=dict(audio_key=str(audio_key))
        )
        assert response.status_code == 200
        payload = response.json()
        if payload is None:
            continue
        result = asr.TranscribeResult.model_validate(payload)
    assert result is not None
    assert result.language == language
    actual_segments = [seg.text.strip() for seg in result.segments]
    assert actual_segments == segments


@pytest.mark.asyncio
async def test_get_random_task(
    nlp_api_client: httpx.AsyncClient,
) -> None:
    ROUTE = "/transcribe/task"

    audio_key = uuid.uuid4()
    response = await nlp_api_client.get(ROUTE, params=dict(audio_key=str(audio_key)))
    assert response.status_code == 200
    body = response.json()
    assert body is None
