from common import asr
from fastapi import Depends, FastAPI, Request

from nlp_api.types import S3Client
from nlp_api.schemas.config import ApiCfg, S3Settings, QueueModeSettings
from nlp_api.schemas.state import ApiState, HttpModeState, QueueModeState


def get_app(request: Request) -> FastAPI:
    return request.app


def get_api_state(app: FastAPI = Depends(get_app)) -> ApiState:
    return app.state.api_state


def get_http_mode_state(state: ApiState = Depends(get_api_state)) -> HttpModeState:
    if state.http_mode_state is None:
        raise ValueError("api is not running in http mode")
    return state.http_mode_state


def get_queue_mode_state(state: ApiState = Depends(get_api_state)) -> QueueModeState:
    if state.queue_mode_state is None:
        raise ValueError("api is not running in queue mode")
    return state.queue_mode_state


def get_asr_model(state: HttpModeState = Depends(get_http_mode_state)) -> asr.AsrModel:
    return state.asr_model


def get_api_cfg(app: FastAPI = Depends(get_app)) -> ApiCfg:
    return app.state.api_cfg


def get_queue_mode_settings(cfg: ApiCfg = Depends(get_api_cfg)) -> QueueModeSettings:
    if cfg.queue_mode_settings is None:
        raise ValueError("api is not running in queue mode")
    return cfg.queue_mode_settings


def get_s3_settings(
    cfg: QueueModeSettings = Depends(get_queue_mode_settings),
) -> S3Settings:
    return cfg.s3


def get_s3_client(state: QueueModeState = Depends(get_queue_mode_state)) -> S3Client:
    return state.s3_client
