from fastapi import Depends, FastAPI, Request

from .state import ApiState


def get_app(request: Request) -> FastAPI:
    return request.app  # type: ignore


def get_api_state(app: FastAPI = Depends(get_app)) -> ApiState:
    return app.state.api_state  # type: ignore
