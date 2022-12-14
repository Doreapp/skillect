"""Basis for CRUD-able resources"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Basis for a CRUD-able resource"""

    # Avoid pylint warnings related to "id" variable
    # pylint: disable=redefined-builtin

    # pylint: disable=no-self-use

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        :param model: A SQLAlchemy model class
        :param schema: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a resource by its id
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get several resources

        :param skip: Offset, i.e. number of resources to skip
        :param limit: Count of resources to fetch
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def _put(self, db: Session, obj: ModelType):  # pylint: disable=no-self-use
        """
        Put an object in the database and update the instance
        """
        db.add(obj)
        db.commit()
        db.refresh(obj)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new resource

        :param obj_in: Resource to persist
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        self._put(db, db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing resource

        :param db_obj: Resource currently saved in the database
        :param obj_in: Resource to replace the old one with
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self._put(db, db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Remove a resource by its id"""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
