import httpx
import pytest
from common import stt

from echo_hub_tests.const import DATA_AUDIO_ROOT


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["filename", "language", "segments"],
    [
        ("hello_there.mp3", "en", ["Hello there."]),
    ],
)
async def test_speech_to_text(
    filename: str,
    language: str,
    segments: list[str],
    nlp_api_client: httpx.AsyncClient,
) -> None:
    audio_path = DATA_AUDIO_ROOT / filename
    assert audio_path.exists(), f"expected {audio_path=} to exist"

    with open(audio_path, "rb") as file:
        files = {"audio": (file.name, file, "audio/mpeg")}
        response = await nlp_api_client.post("/speech_to_text", files=files)
    assert response.status_code == 200
    result = stt.SpeechToTextResult.model_validate(response.json())
    assert result.language == language
    actual_segments = [seg.text.strip() for seg in result.segments]
    assert actual_segments == segments
