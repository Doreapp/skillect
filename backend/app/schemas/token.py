"""Tokens schemas"""

from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Token(BaseModel):
    """Token schema"""

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Token payload schema"""

    sub: Optional[int] = None
