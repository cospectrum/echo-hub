# echo-hub
[![github]](https://github.com/cospectrum/echo-hub)
[![ci]](https://github.com/cospectrum/echo-hub/actions)

[github]: https://img.shields.io/badge/github-cospectrum/echo--hub-8da0cb?logo=github
[ci]: https://github.com/cospectrum/echo-hub/workflows/ci/badge.svg

Natural language processing service.

## Getting started

### start
```sh
docker compose up -d --wait
```

### test
```sh
export NLP_API_URL=http://localhost:6001
uv run coverage run -m pytest .
```

### down
```sh
docker compose down -v
```

## Packages

## nlp-api
The [nlp-api](./packages/nlp-api/) is a configurable API that can operate in multiple modes,
including `http_mode`, `queue_mode`, or both.

In `http_mode`, the nlp-api maintains the `SpeechToText` model in its state and runs the model
directly via the POST `/speech_to_text` endpoint.

In `queue_mode`, the nlp-api provides a POST route `/speech_to_text/task`.
This route saves the audio file to `S3`, sends the task (`audio_key`) to `rabbitmq`, and returns the `audio_key` to the client.
The task is later processed by the `stt-worker`, and the result can be checked using the GET `/speech_to_text/task` route in the nlp-api.
This route simply verifies whether the result exists in the database.

## stt-worker
The [stt-worker](./packages/stt-worker/) is a long-running process (or processes) that consumes tasks (`audio_key`s) from `rabbitmq`.
It retrieves the corresponding audio file from `S3`, runs the `speech_to_text` model, and saves the `result` to the database.
