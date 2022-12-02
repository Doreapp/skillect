"""Schools API entrypoints"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.school import CRUDSchool
from app.models.user import User
from app.schemas.school import School, SchoolCreate


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

    @router.post("/", response_model=School)
    def create_school(
        *,
        db: Session = Depends(deps.get_db),
        school_in: SchoolCreate,
        _: User = Depends(deps.get_current_superuser),
    ) -> School:
        """
        Create new school.

        Needs to be superuser.
        """
        school = school_crud.create(db, obj_in=school_in)
        return school

    return router
