#defines the structure of the database table. So in this case,
#what the incidents table looks like and what type of data each column stores.

# Import SQLAlchemy types and ORM tools
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Base class for all our SQLAlchemy database models
class Base(DeclarativeBase):
    pass


# Database model representing an incident
class IncidentDB(Base):
    __tablename__ = "incidents"

    # Unique identifier for the incident
    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    # Human-readable title of the incident
    title: Mapped[str] = mapped_column(String(200))

    # Detailed description of what happened
    description: Mapped[str] = mapped_column(String)

    # Name of the affected service
    service: Mapped[str] = mapped_column(String(100))

    # Incident severity: LOW, MEDIUM, HIGH, or CRITICAL
    severity: Mapped[str] = mapped_column(String(20))

    # Current lifecycle status of the incident
    status: Mapped[str] = mapped_column(String(30))

    # Time when the incident was created
    created_at: Mapped[datetime] = mapped_column(DateTime)

    # Time when the incident was last updated
    updated_at: Mapped[datetime] = mapped_column(DateTime)