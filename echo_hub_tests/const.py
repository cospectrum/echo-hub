import os
import pathlib

NLP_API_URL = os.getenv("NLP_API_URL", "http://localhost:6001")

TESTS_ROOT = pathlib.Path(__file__).parent
PROJECT_ROOT = TESTS_ROOT.parent
DATA_ROOT = PROJECT_ROOT / "data"
DATA_AUDIO_ROOT = DATA_ROOT / "audio"
