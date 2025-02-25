# nlp-worker
Consumes tasks from the queue and writes the results to db.

## Dev

```sh
CFG_PATH=./config.json uv run main.py
```

## Details

Script `./main.py` expects json cfg passed via `CFG_PATH` env variable.
See [./config.json](./config.json) for example.
