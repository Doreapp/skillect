"""Schools API entrypoints"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.school import CRUDSchool
from app.schemas.school import School


def get_router() -> APIRouter:
    """Build and return schools' router"""
    router = APIRouter()
    school_crud = CRUDSchool()

    @router.get("/", response_model=List[School])
    def read_schools(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
    ) -> List[School]:
        """
        Retrieve schools.
        """
        return school_crud.get_multi(db, skip=skip, limit=limit)

    return router
