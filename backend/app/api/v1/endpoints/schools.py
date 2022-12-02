"""Schools API entrypoints"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.school import CRUDSchool
from app.models.user import User
from app.schemas.school import School, SchoolCreate, SchoolUpdate


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

    @router.get("/{school_id}", response_model=School)
    def read_school_by_id(
        school_id: int,
        db: Session = Depends(deps.get_db),
    ) -> Optional[School]:
        """
        Get a single school from its id.
        """
        school = school_crud.get(db, id=school_id)
        if not school:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No school with this id exists",
            )
        return school

    @router.put("/{school_id}", response_model=School)
    def update_school(
        *,
        db: Session = Depends(deps.get_db),
        school_id: int,
        school_in: SchoolUpdate,
        _: User = Depends(deps.get_current_superuser),
    ) -> Optional[School]:
        """
        Update a school.

        Needs to be superuser.
        """
        school = school_crud.get(db, id=school_id)
        if not school:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No school with this id exists",
            )
        school = school_crud.update(db, db_obj=school, obj_in=school_in)
        return school

    return router
