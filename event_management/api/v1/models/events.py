from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import pytz
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    """
    SQLAlchemy model representing an event.

    Attributes:
        id (int): Primary key, unique identifier of the event.
        name (str): Name of the event.
        location (str): Location where the event will take place.
        start_time (datetime): Event start time with timezone information.
        end_time (datetime): Event end time with timezone information.
        max_capacity (int): Maximum number of attendees allowed.
        created_at (datetime): Timestamp when the event was created, defaulting to current UTC time.
        updated_at (datetime): Timestamp when the event was last updated, auto-updated on modification.
        attendees (List[Attendee]): List of attendees registered for this event.
    """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    location = Column(String(500), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    max_capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(pytz.UTC),
        onupdate=lambda: datetime.now(pytz.UTC),
    )
    attendees = relationship(
        "Attendee", back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', location='{self.location}')>"


class Attendee(Base):
    """
    SQLAlchemy model representing an attendee registered for an event.

    Attributes:
        id (int): Primary key, unique identifier of the attendee.
        name (str): Name of the attendee.
        email (str): Email address of the attendee.
        event_id (int): Foreign key referencing the associated event.
        registered_at (datetime): Timestamp when the attendee registered, defaulting to current UTC time.
        event (Event): Relationship back to the associated Event.

    Constraints:
        unique_email_per_event: Ensures an attendee's email is unique per event.
    """

    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registered_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC)
    )
    event = relationship("Event", back_populates="attendees")

    __table_args__ = (
        UniqueConstraint("email", "event_id", name="unique_email_per_event"),
    )

    def __repr__(self):
        return f"<Attendee(id={self.id}, name='{self.name}', email='{self.email}')>"
