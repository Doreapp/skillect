"""Script to initiate the database"""

import logging

from sqlalchemy.orm import Session

from app.crud.school import CRUDSchool
from app.db import base
from app.schemas.school import SchoolCreate

LOGGER = logging.getLogger(__file__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def create_mock_schools(crud: CRUDSchool, db: Session):
    """Create mock schools in the database"""
    LOGGER.info("Creating mock schools")
    school1 = SchoolCreate(name="INSA Lyon", description="Ecole d'ingénieur post bac, topitop")
    crud.create(db, obj_in=school1)
    school2 = SchoolCreate(name="KTH", description="Ecole d'ingénieur à Stockholm", link="")
    crud.create(db, obj_in=school2)


def init_db(db: Session) -> None:
    """Initiate the database"""
    LOGGER.info("Initiating database with session %s", db.bind)
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables using the following line (create_all)
    base.Base.metadata.create_all(bind=db.get_bind())  # pylint: disable=no-member
    crud_school = CRUDSchool()
    schools = crud_school.get_multi(db)
    if len(schools) == 0:
        create_mock_schools(crud_school, db)
        schools = crud_school.get_multi(db)
