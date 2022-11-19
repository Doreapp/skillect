"""Script to initiate the database"""

import logging

from sqlalchemy.orm import Session

from app.core.config import SETTINGS
from app.crud.school import CRUDSchool
from app.crud.user import CRUDUser
from app.db import base
from app.schemas.school import SchoolCreate
from app.schemas.user import UserCreate

LOGGER = logging.getLogger(__file__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def create_mock_schools(crud: CRUDSchool, db: Session):
    """Create mock schools in the database if db empty"""
    schools = crud.get_multi(db)
    if len(schools) == 0:
        LOGGER.info("Creating mock schools")
        school1 = SchoolCreate(name="INSA Lyon", description="Ecole d'ingénieur post bac, topitop")
        crud.create(db, obj_in=school1)
        school2 = SchoolCreate(name="KTH", description="Ecole d'ingénieur à Stockholm", link="")
        crud.create(db, obj_in=school2)


def create_first_superuser(crud: CRUDUser, db: Session):
    """Create the first superuser in the db if needed"""
    user = crud.get_by_email(db, email=SETTINGS.FIRST_SUPERUSER)
    if not user:
        LOGGER.info("Creating first super user")
        user_in = UserCreate(
            email=SETTINGS.FIRST_SUPERUSER,
            password=SETTINGS.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create(db, obj_in=user_in)


def init_db(db: Session) -> None:
    """Initiate the database"""
    LOGGER.info("Initiating database with session %s", db.bind)
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables using the following line (create_all)
    base.Base.metadata.create_all(bind=db.get_bind())  # pylint: disable=no-member
    create_mock_schools(CRUDSchool(), db)
    create_first_superuser(CRUDUser(), db)
