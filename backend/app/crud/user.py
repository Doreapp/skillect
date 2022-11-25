"""Create, Read, Update and Delete functions for users """

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# pylint: disable=no-self-use


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD instance for users"""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get a user by its email

        :param db: Database connexion
        :param email: Email to search for
        :return: User if found, None elsewere
        """
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new user from a `UserCreate` model

        :param db: Database connexion
        :param obj_in: Object storing the informations to create a user with
        :return: The user created
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        self._put(db, db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Update an existing user

        :param db: Database connexion
        :param db_obj: Object currently stored in the database
        :param obj_in: Object updated, replacing the `db_obj`
        :return: The updated user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user

        :param db: Database connexion
        :param email: User email, to use for identification
        :param password: Plain text password, to connect the user with
        :return: User if the authentication succeed, None elsewere
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: User) -> bool:
        """
        Return if given `user` is active
        """
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        """
        Return if given `user` is super user
        """
        return user.is_superuser
