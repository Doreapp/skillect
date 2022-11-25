"""API first version"""

from fastapi import APIRouter

from .endpoints import login, schools, users


def get_api_router() -> APIRouter:
    """Build and return the API router"""
    api_router = APIRouter()
    api_router.include_router(login.get_router(), tags=["login"])
    api_router.include_router(users.get_router(), prefix="/users", tags=["users"])
    api_router.include_router(schools.get_router(), prefix="/school", tags=["schools"])
    return api_router
