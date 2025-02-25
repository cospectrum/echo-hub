# nlp-worker
`nlp-worker` consumes tasks from the queue and writes the results to db.

The entry point is the script `main.py`, which expects the json cfg to be passed via `CFG_PATH` env variable.
See [./config.json](./config.json) for example.

## Dev
```sh
CFG_PATH=./config.json uv run main.py
```
