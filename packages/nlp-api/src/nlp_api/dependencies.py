from fastapi import Depends, FastAPI, Request

from .state import ApiState


def get_app(request: Request) -> FastAPI:
    return request.app


def get_api_state(app: FastAPI = Depends(get_app)) -> ApiState:
    return app.state.api_state
