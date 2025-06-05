from pydantic import BaseModel, EmailStr, field_validator, validator, Field
from datetime import datetime
from typing import List, Optional, Union
import pytz


class EventBase(BaseModel):
    name: str
    location: str
    start_time: Union[str, datetime]
    end_time: Union[str, datetime]
    max_capacity: int

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            try:
                if len(v) == 10:  # Format: "2025-07-01"
                    v = datetime.fromisoformat(v + "T09:00:00")
                else:
                    v = datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(
                    "start_time must be a valid date/datetime string (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
                )

        if v.tzinfo is None:
            v = pytz.timezone("Asia/Kolkata").localize(v)

        if v <= datetime.now(pytz.UTC):
            raise ValueError("start_time must be in the future.")

        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: Union[str, datetime], info) -> datetime:
        if isinstance(v, str):
            try:
                if len(v) == 10:  # Format: "2025-07-02"
                    v = datetime.fromisoformat(v + "T18:00:00")
                else:
                    v = datetime.fromisoformat(v)
            except ValueError:
                raise ValueError(
                    "end_time must be a valid date/datetime string (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
                )

        if v.tzinfo is None:
            v = pytz.timezone("Asia/Kolkata").localize(v)

        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_after_start(cls, v: datetime, info) -> datetime:
        if "start_time" in info.data:
            start_time = info.data["start_time"]
            if isinstance(start_time, str):
                if len(start_time) == 10:
                    start_time = datetime.fromisoformat(start_time + "T09:00:00")
                else:
                    start_time = datetime.fromisoformat(start_time)
                if start_time.tzinfo is None:
                    start_time = pytz.timezone("Asia/Kolkata").localize(start_time)

            if v <= start_time:
                raise ValueError("end_time must be after start_time")

        return v


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, min_length=1, max_length=500)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_capacity: Optional[int] = Field(None, gt=0, le=10000)


class AttendeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Attendee name")
    email: EmailStr = Field(..., description="Attendee email address")


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeResponse(AttendeeBase):
    id: int
    registered_at: datetime

    class Config:
        from_attributes = True


class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    attendee_count: int = 0

    class Config:
        from_attributes = True


class EventWithAttendees(EventResponse):
    attendees: List[AttendeeResponse] = []


class PaginatedAttendeesResponse(BaseModel):
    attendees: List[AttendeeResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class PaginatedEventsResponse(BaseModel):
    events: List[EventResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
