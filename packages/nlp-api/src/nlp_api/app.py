from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator

from . import middlewares
from .config.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

app.middleware("http")(middlewares.log_request_info)
app.middleware("http")(middlewares.add_trace_id)
