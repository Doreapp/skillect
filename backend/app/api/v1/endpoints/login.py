"""Endpoint to login as a user"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import SETTINGS
from app.core.security import get_password_hash
from app.crud.user import CRUDUser
from app.models.user import User as UserModel
from app.schemas.msg import Msg
from app.schemas.token import Token
from app.schemas.user import User as UserSchema
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)


def get_router() -> APIRouter:
    """Build and return login router"""
    router = APIRouter()
    user_crud = CRUDUser()

    @router.post("/login/access-token", response_model=Token)
    def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
    ) -> Any:
        """
        OAuth2 compatible token login, get an access token for future requests

        - Raise HTTP 400 if the pair email/password is incorrect or the user is inactive

        Takes a login form data as input. It must contain `username` and `password`.

        Returns JSON data with `access_token` and `token_type`
        """
        user = user_crud.authenticate(db, email=form_data.username, password=form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
            )
        if not user_crud.is_active(user):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        access_token_expires = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

    @router.post("/password-recovery/{email}", response_model=Msg)
    def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
        """
        Password Recovery

        - Raise HTTP 404 if user not found

        Takes a user as input and sends him/her a Reset-password email

        Returns a validation message
        """
        user = user_crud.get_by_email(db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user with this username does not exist in the system.",
            )
        password_reset_token = generate_password_reset_token(email=email)
        send_reset_password_email(email_to=user.email, email=email, token=password_reset_token)
        return {"msg": "Password recovery email sent"}

    @router.post("/reset-password/", response_model=Msg)
    def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(deps.get_db),
    ) -> Any:
        """
        Reset password

        - Raises HTTP 404 if user not found
        - Raises HTTP 400 if token invalid

        Takes a verfication token and the new password as input.

        Returns a validation message.
        """
        email = verify_password_reset_token(token)
        if not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        user = user_crud.get_by_email(db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user with this username does not exist in the system.",
            )
        if not user_crud.is_active(user):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        hashed_password = get_password_hash(new_password)
        user.hashed_password = hashed_password
        db.add(user)
        db.commit()
        return {"msg": "Password updated successfully"}

    return router
