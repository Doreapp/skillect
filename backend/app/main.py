"""Main entrypoint of the server"""

import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.v1 import get_api_router
from .core.config import SETTINGS

LOGGER = logging.getLogger("uvicorn.error")
LOGGER.info("Starting the server")

# 'app' will be found by gunicorn
app = FastAPI(title="skillect", openapi_url=f"{SETTINGS.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if SETTINGS.BACKEND_CORS_ORIGINS:
    LOGGER.debug("Allowing CORS from: %s", ", ".join(SETTINGS.BACKEND_CORS_ORIGINS))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in SETTINGS.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(get_api_router(), prefix=SETTINGS.API_V1_STR)
