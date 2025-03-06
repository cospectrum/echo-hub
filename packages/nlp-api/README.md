# nlp-api
An API that can convert `speech to text` in both synchronous and asynchronous modes.

## Dev
start fastapi app:
```sh
CFG_PATH=./configs/http_mode.json uv run fastapi dev src/nlp_api/app.py
```

## Docs
To view swagger, go to `http://host:port/docs`.
Note that API depends on the configured `mode`.
The API mode is determined from the cfg file (passed via `CFG_PATH` env variable).
