# main.py

from fastapi import FastAPI
import uvicorn

from . import models
from .database import engine
from .routers import blogs_routes, users_routes, auth_routes


app = FastAPI()


@app.get('/')
def root():
    return {'detail': {'deploy': 'successfully',
                       'Visit': 'https://fast-api-first.vercel.app/docs'}}


models.Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)

app.include_router(blogs_routes.router)

app.include_router(users_routes.router)
