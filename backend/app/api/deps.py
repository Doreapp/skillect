"""Common dependencies"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import SETTINGS
from app.crud.user import CRUDUser
from app.db.session import SessionLocal
from app.models.user import User as UserModel
from app.schemas.token import TokenPayload

REUSABLE_OAUTH2 = OAuth2PasswordBearer(tokenUrl=f"{SETTINGS.API_V1_STR}/login/access-token")


def get_db() -> Generator:
    """Returns database session"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(REUSABLE_OAUTH2)
) -> UserModel:
    """
    Return the current authenticated user from an access token

    - Raise HTTP 403 (Forbidden) if unable to decode token
    - Raise HTTP 404 (Not found) if user not found

    :param db: Database session
    :param token: Token identifying the current user
    :return: Current User
    """
    try:
        payload = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from exc
    user = CRUDUser().get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Check that current user is active

    - Raise HTTP 400 (Bad request) if user inactive

    :param current_user: Authenticated user (given passed token)
    :return: Current and active user
    """
    if not CRUDUser.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_superuser(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Check that current user if superuser

    - Raise HTTP 400 (Bad request) if user isn't superuser

    :param current_user: Currently authenticated user
    :return: User that is super user
    """
    if not CRUDUser.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return current_user
