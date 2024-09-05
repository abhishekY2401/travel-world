import secrets
from typing import Any, Annotated, Optional
import os

from pydantic import AnyHttpUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    ENV: Optional[str] = "dev"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 30
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30
    JWT_ALGO: str = "HS512"
    SERVER_NAME: str = "fastapi-server"
    SERVER_HOST: str = "localhost"
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str = "travel-app"
    PROJECT_DESCRIPTION: Optional[str] = None
    PROJECT_VERSION: Optional[str] = None

    # Database COMPONENT SETTINGS
    MONGO_DATABASE: str
    MONGO_DATABASE_URI: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
