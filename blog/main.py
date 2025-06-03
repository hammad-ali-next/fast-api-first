# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from . import models
from .database import engine
from .routers import blogs_routes, users_routes, auth_routes


app = FastAPI()

origins = [
    "http://localhost:3000",  # <-- your frontend origin exactly
    "http://127.0.0.1:3000",
    # "https://my-blog-app.vercel.app/",
    "https://my-blog-app-kappa-gold.vercel.app"
    # add more if needed
]

# cors added
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allow any origin
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allow all headers
)


@app.get('/')
def root():
    return {'detail': {'deploy': 'successfully',
                       'Visit': 'https://fast-api-first.vercel.app/docs'}}


models.Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)

app.include_router(blogs_routes.router)

app.include_router(users_routes.router)
