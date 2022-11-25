"""Security-related utilities"""

from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import SETTINGS

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""Context for hasing and verifying passwords"""

ALGORITHM = "HS256"
"""Hashing alogirthm for passwords"""


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Create a secure access token. Can be used to identify a user previously authenticated.

    :param subject: Subject to encode in the token
    :param expires_delta: Duration of the access token. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES
    :return: encoded Json Web Token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SETTINGS.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against an hashed password

    :param plain_password: Plain text password, to check
    :param hashed_password: Hash to confront
    :return: Whether the password matches the hash
    """
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Create an hashed password from a plain text password

    :param password: Plain text password, to hash
    :return: Hashed password (storable in database, for instance)
    """
    return PASSWORD_CONTEXT.hash(password)
