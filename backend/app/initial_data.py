"""Script to initialize the database"""

import logging

from .db.init_db import init_db
from .db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


def init():
    """Init the DB"""
    db = SessionLocal()
    init_db(db)


def main():
    """Main function"""
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
