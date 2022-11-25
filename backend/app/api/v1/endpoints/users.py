"""API endpoints related to users"""

import logging
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr  # pylint: disable=no-name-in-module
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import SETTINGS
from app.crud.user import CRUDUser
from app.models.user import User as UserModel
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate, UserUpdate

LOGGER = logging.getLogger(__name__)


def get_router() -> APIRouter:
    """Build and return users' router"""
    router = APIRouter()
    user_crud = CRUDUser()

    @router.get("/", response_model=List[UserSchema])
    def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        _: UserModel = Depends(deps.get_current_superuser),
    ) -> Any:
        """
        Retrieve all users.

        Needs to be superuser.
        """
        users = user_crud.get_multi(db, skip=skip, limit=limit)
        return users

    @router.post("/", response_model=UserSchema)
    def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserCreate,
        _: UserModel = Depends(deps.get_current_superuser),
    ) -> Any:
        """
        Create new user.

        Needs to be superuser.
        """
        user = user_crud.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this username already exists in the system.",
            )
        user = user_crud.create(db, obj_in=user_in)
        LOGGER.info("New user created %s(%s)", user.full_name, user.email)
        return user

    @router.put("/me", response_model=UserSchema)
    def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: UserModel = Depends(deps.get_current_active_user),
    ) -> Any:
        """
        Update own user.
        """
        current_user_data = jsonable_encoder(current_user)
        user_in = UserUpdate(**current_user_data)
        if password is not None:
            user_in.password = password
        if full_name is not None:
            user_in.full_name = full_name
        if email is not None:
            user_in.email = email
        user = user_crud.update(db, db_obj=current_user, obj_in=user_in)
        return user

    @router.get("/me", response_model=UserSchema)
    def read_user_me(
        current_user: UserModel = Depends(deps.get_current_active_user),
    ) -> Any:
        """
        Get current user.
        """
        return current_user

    @router.post("/open", response_model=UserSchema)
    def create_user_open(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(None),
    ) -> Any:
        """
        Create new user without the need to be logged in.
        """
        if not SETTINGS.USERS_OPEN_REGISTRATION:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Open user registration is forbidden on this server",
            )
        user = user_crud.get_by_email(db, email=email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this username already exists in the system",
            )
        user_in = UserCreate(password=password, email=email, full_name=full_name)
        user = user_crud.create(db, obj_in=user_in)
        return user

    @router.get("/{user_id}", response_model=UserSchema)
    def read_user_by_id(
        user_id: int,
        current_user: UserModel = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
    ) -> Any:
        """
        Get a specific user by id.
        """
        user = user_crud.get(db, id=user_id)
        if user == current_user:
            return user
        if not user_crud.is_superuser(current_user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user doesn't have enough privileges",
            )
        return user

    @router.put("/{user_id}", response_model=UserSchema)
    def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: UserUpdate,
        _: UserModel = Depends(deps.get_current_superuser),
    ) -> Any:
        """
        Update a user.

        Needs to be superuser.
        """
        user = user_crud.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user with this username does not exist in the system",
            )
        user = user_crud.update(db, db_obj=user, obj_in=user_in)
        return user

    return router
