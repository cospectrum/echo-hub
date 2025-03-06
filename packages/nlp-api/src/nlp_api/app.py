from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .lifespan import lifespan

app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)
