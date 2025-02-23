from fastapi import FastAPI

from .lifespan import lifespan


app = FastAPI(lifespan=lifespan)
