# echo-hub
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
