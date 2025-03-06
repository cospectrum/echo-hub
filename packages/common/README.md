# common
Common utils

## modules

### stt
Provides `SpeechToTextModel` interface and some useful `schemas`:
- `SpeechToTextResult` - output of speech to text model.
- `SpeechToTextTask` - task for `stt-worker` (rabbitmq msg).
- `WhisperCfg` - used as json cfg for `whisper model`.
