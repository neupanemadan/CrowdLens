from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.core.config import settings
from app.db.base import Base, engine

# Ensure upload directories exist before app starts (needed for StaticFiles mount)
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
settings.upload_original_path.mkdir(parents=True, exist_ok=True)
settings.upload_annotated_path.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded/annotated images as static files
app.mount("/media", StaticFiles(directory=settings.UPLOAD_DIR), name="media")

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
