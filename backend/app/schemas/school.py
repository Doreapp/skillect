"""School schema"""

from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class SchoolBase(BaseModel):
    """Shared properties"""

    name: str
    description: Optional[str] = None
    link: Optional[str] = None


class SchoolCreate(SchoolBase):
    """Properties to receive on school creation"""


class SchoolUpdate(SchoolBase):
    """Properties to receive on item update"""


class SchoolInDBBase(SchoolBase):
    """Properties shared by models stored in DB"""

    id: int

    class Config:
        """Configuration class needed by pydandic"""

        orm_mode = True


class School(SchoolInDBBase):
    """Properties to return to client"""


class SchoolInDB(SchoolInDBBase):
    """Properties stored in DB"""
