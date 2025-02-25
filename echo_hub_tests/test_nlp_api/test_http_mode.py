import pytest
import httpx

from common import asr
from echo_hub_tests.const import DATA_ROOT


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["filename", "language", "segments"],
    [
        ("hello_there.mp3", "en", ["Hello there."]),
    ],
)
async def test_transcribe(
    filename: str,
    language: str,
    segments: str,
    nlp_api_client: httpx.AsyncClient,
) -> None:
    audio_path = DATA_ROOT / "audio" / filename
    assert audio_path.exists(), f"expected {audio_path=} to exist"

    with open(audio_path, "rb") as file:
        files = {"audio": (file.name, file, "audio/mpeg")}
        response = await nlp_api_client.post("/transcribe", files=files)
    assert response.status_code == 200
    result = asr.TranscribeResult.model_validate(response.json())
    assert result.language == language
    actual_segments = [seg.text.strip() for seg in result.segments]
    assert actual_segments == segments
