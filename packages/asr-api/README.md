# asr-api

## Docs

To view swagger, go to `host:port/docs`.
Note that API depends on the configured `mode`.
The API mode is determined from the cfg file (passed via `CFG_PATH` env variable).

### Http mode
To run the `asr-api` in this mode, pass the config in the following format:
```sh
{
    "http_mode_settings": {
        "asr_model": {
            "type": "whisper",
            "cfg": {}
        }
    }
}
```

### Queue mode
In this mode, the api will be able to send tasks to rabbitmq.
The result will be saved in postgres, so you also need to specify its settings.
Config example:
```sh
{
    "queue_mode_settings": {
        "s3": {
            "base_url": "http://localhost:9000"
        },
        "rabbitmq": {
            "url": "amqp://user:pass@localhost:5672"
        },
        "postgres": {
            "url": "postgres://user:pass@localhost:5432"
        }
    }
}
```

### Http and queue mode
In this mode, the api takes over the functionality of both modes that were described above.
To launch in this mode, combine http and queue configurations together:
```sh
{
    "queue_mode_settings": {...},
    "http_mode_settings": {...}
}
```


## Dev
```sh
CFG_PATH=./configs/http_mode.json uv run fastapi dev src/asr_api/app.py
```
