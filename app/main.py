from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .routers import routes


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = [
    "http://127.0.0.1:5000",
    "http://127.0.0.1:8000",
    "http://localhost:5000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

