# stt-worker
`Speech to text` worker.

## Run
The entry point of worker is the script `main.py`, which expects the json cfg to be passed via `CFG_PATH` env variable.
See [./config.json](./config.json) for example.

```sh
CFG_PATH=./config.json uv run main.py
```

To spawn multiple workers, simply run the script the required number of times.
