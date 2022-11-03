"""Script to wait for the Database to come online"""

import logging
from time import sleep
from typing import Tuple

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__file__)

# Wait maximum 5 minutes
MAX_TRIES = 60 * 5
WAIT_SECONDS = 1


def connect() -> Tuple[bool, Exception]:
    """Try to connect to the Database, return if it was successful"""
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except SQLAlchemyError as exception:
        return False, exception
    return True, None


def main():
    """Main entrypoint of the script"""
    LOGGER.info("Initializing service")
    connection_ok = False
    attempt_count = 0
    exception = None
    while not connection_ok and attempt_count < MAX_TRIES:
        if attempt_count > 0:
            LOGGER.info("Connection to database failed, retrying")
        attempt_count += 1
        connection_ok, exception = connect()
        if not connection_ok:
            sleep(WAIT_SECONDS)
    if not connection_ok:
        raise Exception("Unable to connect to the database") from exception
    LOGGER.info("Service initialized")


if __name__ == "__main__":
    main()
