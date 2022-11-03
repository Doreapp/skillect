"""API first version"""

from fastapi import APIRouter

from .endpoints import schools


def get_api_router() -> APIRouter:
    """Build and return the API router"""
    api_router = APIRouter()
    api_router.include_router(schools.get_router(), prefix="/school", tags=["schools"])
    return api_router
