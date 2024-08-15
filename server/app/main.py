
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(api_router, prefix=settings.API_V1_STR)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=app_init
)

# Setting all CORS enabled origin
if settings.BACKEND_CORS_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        # Trailing slash causes CORS failures from these supported domains
        allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],  # noqa
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
