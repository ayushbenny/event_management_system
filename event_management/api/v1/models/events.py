from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import pytz
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
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
