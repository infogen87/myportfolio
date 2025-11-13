from uuid import uuid4
from sqlalchemy import (Column, func, DateTime, Text, Numeric, Integer)
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class ProjectsDB(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), default=uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    github_link = Column(Text, nullable=False)
    live_link = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)