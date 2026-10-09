from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR, PANELS_DIR, EXPORTS_DIR, settings
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    yield

app = FastAPI(
    title=settings.app_name,
    description="AI comic story creator based on the supplied ComicCraft specification.",
    version="1.0.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(router)
