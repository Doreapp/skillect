"""CRUD for schools"""

from app.crud.base import CRUDBase
from app.models import School
from app.schemas.school import SchoolCreate, SchoolUpdate


class CRUDSchool(CRUDBase[School, SchoolCreate, SchoolUpdate]):
    """CRUD class for School resource"""

    def __init__(self):
        super().__init__(School)
