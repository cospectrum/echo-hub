import uuid

import httpx
import pytest
from common import stt

from echo_hub_tests.const import DATA_AUDIO_ROOT
from echo_hub_tests.utils import backoff


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["filename", "language", "segments"],
    [
        ("hello_there.mp3", "en", ["Hello there."]),
    ],
)
async def test_speech_to_text_task(
    filename: str,
    language: str,
    segments: list[str],
    nlp_api_client: httpx.AsyncClient,
) -> None:
    ROUTE = "/speech_to_text/task"
    audio_path = DATA_AUDIO_ROOT / filename
    assert audio_path.exists(), f"expected {audio_path=} to exist"

    with open(audio_path, "rb") as file:
        files = {"audio": (file.name, file, "audio/mpeg")}
        response = await nlp_api_client.post(ROUTE, files=files)
    assert response.status_code == 200

    body = response.json()
    audio_key = uuid.UUID(body)
    result = None
    coro = nlp_api_client.get(ROUTE, params={"audio_key": str(audio_key)})
    response = await backoff(coro)
    assert response.status_code == 200

    result = stt.SpeechToTextResult.model_validate(response.json())
    assert result.language == language
    actual_segments = [seg.text.strip() for seg in result.segments]
    assert actual_segments == segments


@pytest.mark.asyncio
async def test_get_random_task(
    nlp_api_client: httpx.AsyncClient,
) -> None:
    ROUTE = "/speech_to_text/task"

    audio_key = uuid.uuid4()
    response = await nlp_api_client.get(ROUTE, params=dict(audio_key=str(audio_key)))
    assert response.status_code == 200
    body = response.json()
    assert body is None
