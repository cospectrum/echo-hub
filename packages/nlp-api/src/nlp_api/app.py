from fastapi import FastAPI

from . import middlewares
from .config.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

app.middleware("http")(middlewares.log_request_info)
app.middleware("http")(middlewares.add_trace_id)
