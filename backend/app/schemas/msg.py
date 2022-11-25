"""Message schema"""

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Msg(BaseModel):
    """Message schema"""

    msg: str
