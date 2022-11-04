"""Main entrypoint of the server"""

import logging

from fastapi import FastAPI

from .api.v1 import get_api_router
from .core.config import SETTINGS

LOGGER = logging.getLogger(__file__)
LOGGER.info("Starting the server")

# 'app' will be found by gunicorn
app = FastAPI(title="skillect", openapi_url=f"{SETTINGS.API_V1_STR}/openapi.json")
app.include_router(get_api_router(), prefix=SETTINGS.API_V1_STR)
