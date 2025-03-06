# nlp-api
An API that can convert `speech to text` in both synchronous and asynchronous modes.

## Dev
start fastapi app (in http_mode):
```sh
CFG_PATH=./configs/http_mode.json uv run fastapi dev src/nlp_api/app.py
```

## Docs
To view swagger, go to `http://host:port/docs`.
Note that API depends on the configured `mode`.
The API mode is determined from the cfg file (passed via `CFG_PATH` env variable).

### Http mode
To run the `nlp-api` in this mode, pass the json config (via `CFG_PATH`) with the `speech_to_text` field.
For example, [./configs/http_mode.json](./configs/http_mode.json).

#### Requests
Transcribe audio:
```sh
curl -X 'POST' \
  'http://host:port/speech_to_text' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'audio=@filename.mp3;type=audio/mpeg'
```

### Queue mode
In this mode, the api will be able to send tasks to `queue`.
To run the `nlp-api` in this mode, pass the json config (via `CFG_PATH`) with the `queue_mode` fields (postgres, rabbitmq, s3, ...).
For example, [./configs/queue_mode.json](./configs/queue_mode.json).

#### Requests
Publish transcribe audio task and get the `audio_key` back:
```sh
curl -X 'POST' \
  'http://host:port/speech_to_text/task' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'audio=@filepath.mp3;type=audio/mpeg'
```

Get the result of the task if it is ready:
```sh
curl -X 'GET' \
  'http://host:port/speech_to_text/task?audio_key=<audio_key>' \
  -H 'accept: application/json'
```

### Http and queue mode
In this mode, the api takes over the functionality of both `queue` and `http` modes that were described above.
To launch in this mode, combine `http` and `queue` configurations into one file.
For example, [./configs/http_and_queue_mode.json](./configs/http_and_queue_mode.json).
