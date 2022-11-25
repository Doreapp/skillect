"""Users schemas"""

from typing import Optional

from pydantic import BaseModel, EmailStr  # pylint: disable=no-name-in-module


class UserBase(BaseModel):
    """Shared properties of a user"""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Properties to receive via API on creation"""

    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """Properties to receive via API on update"""

    password: Optional[str] = None


class UserInDBBase(UserBase):
    """Basic properties saved in the database"""

    id: Optional[int] = None

    class Config:
        """Configuration class needed by pydandic"""

        orm_mode = True


class User(UserInDBBase):
    """Additional properties to return via API"""


class UserInDB(UserInDBBase):
    """Additional properties stored in DB"""

    hashed_password: str
