# echo-hub
[![github]](https://github.com/cospectrum/echo-hub)
[![ci]](https://github.com/cospectrum/echo-hub/actions)

[github]: https://img.shields.io/badge/github-cospectrum/echo--hub-8da0cb?logo=github
[ci]: https://github.com/cospectrum/echo-hub/workflows/ci/badge.svg?branch=main

Natural language processing service.

## docker-compose

```sh
docker-compose build
docker-compose up -d
```
```sh
docker-compose down -v
```

## tests
```sh
export NLP_API_URL=http://localhost:6001
pytest -v tests packages
```

## packages

### nlp-api
See [packages/nlp-api](./packages/nlp-api/) for additional info.
#### Docker
```sh
docker build . -f ./docker/Dockerfile.nlp-api -t echo-hub/nlp-api
docker run -p 6001:80 -e ./packages/nlp-api/configs/http_mode.json echo-hub/nlp-api
```
