"""App configuration"""

import secrets
from typing import Any, Dict, Optional

# pylint is unable to fetch the names from pydantic
# pylint: disable=no-name-in-module
from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    """Application-wide settings"""

    # pylint doesn't like pydantic decorators
    # pylint: disable=no-self-argument, no-self-use

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, value: str) -> Optional[str]:
        """Validator of SENTRY_DSN"""
        if len(value) == 0:
            return None
        return value

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:
        """Validator of SQLALCHEMY_DATABASE_URI"""
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        """Configuration"""

        case_sensitive = True


SETTINGS = Settings()
