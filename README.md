# echo-hub
[![github]](https://github.com/cospectrum/echo-hub)
[![ci]](https://github.com/cospectrum/echo-hub/actions)

[github]: https://img.shields.io/badge/github-cospectrum/echo--hub-8da0cb?logo=github
[ci]: https://github.com/cospectrum/echo-hub/workflows/ci/badge.svg

Natural language processing service.

## Getting Started

### start
```sh
docker compose build
docker compose up -d --wait
```

### test
```sh
export NLP_API_URL=http://localhost:6001
uv run pytest -v .
```

### down
```sh
docker compose down -v
```

## packages

### nlp-api
See [packages/nlp-api](./packages/nlp-api/) for additional info.
#### Separate docker build
```sh
docker build . -f ./docker/Dockerfile.nlp-api -t echo-hub/nlp-api
docker run -p 6001:80 -e CFG_PATH=./packages/nlp-api/configs/http_mode.json echo-hub/nlp-api
```

### nlp-worker
See [packages/nlp-worker](./packages/nlp-worker/) for additional info.
#### Separate docker build
```sh
docker build . -f ./docker/Dockerfile.nlp-worker -t echo-hub/nlp-worker
docker run -e CFG_PATH=./packages/nlp-worker/config.json echo-hub/nlp-worker
```
