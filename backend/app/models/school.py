"""School model"""

from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class School(Base):
    """School model"""

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    link = Column(String)
