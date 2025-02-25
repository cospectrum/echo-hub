# echo-hub
[![github]](https://github.com/cospectrum/echo-hub)
[![ci]](https://github.com/cospectrum/echo-hub/actions)

[github]: https://img.shields.io/badge/github-cospectrum/echo--hub-8da0cb?logo=github
[ci]: https://github.com/cospectrum/echo-hub/workflows/ci/badge.svg

Natural language processing service.

## Getting Started
start:
```sh
docker compose build
docker compose up -d --wait
```

tests:
```sh
export NLP_API_URL=http://localhost:6001
pytest -v tests packages
```

down:
```sh
docker compose down -v
```

## packages

### nlp-api
See [packages/nlp-api](./packages/nlp-api/) for additional info.
#### Docker
```sh
docker build . -f ./docker/Dockerfile.nlp-api -t echo-hub/nlp-api
docker run -p 6001:80 -e ./packages/nlp-api/configs/http_mode.json echo-hub/nlp-api
```

### nlp-worker
See [packages/nlp-worker](./packages/nlp-worker/) for additional info.
