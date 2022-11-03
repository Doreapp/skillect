"""Base class for database-stored resources"""

from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


# pylint: disable=no-self-argument
@as_declarative()
class Base:
    """Base resource"""

    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __repr__(self) -> str:
        """Retrun string representation"""
        attrs = dict(self.__dict__)
        attrs.pop("_sa_instance_state")
        return str(attrs)
