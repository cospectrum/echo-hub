# echo-hub
[![github]](https://github.com/cospectrum/echo-hub)
[![ci]](https://github.com/cospectrum/echo-hub/actions)

[github]: https://img.shields.io/badge/github-cospectrum/echo--hub-8da0cb?logo=github
[ci]: https://github.com/cospectrum/echo-hub/workflows/ci/badge.svg

Natural language processing service.

## asr-api

```sh
docker build . -f ./docker/Dockerfile.asr-api -t echo-hub/asr-api
docker run -p 6001:80 -e ./packages/asr-api/configs/http_mode.json echo-hub/asr-api
```

See [packages/asr-api](./packages/asr-api/) for additional info.
