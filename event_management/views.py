from datetime import datetime, time
import math
from dateutil import parser
from fastapi import HTTPException
from sqlalchemy import and_, select
from typing import List
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
import pytz
from event_management.api.v1.schemas.events import (
    AttendeeCreate,
    AttendeeResponse,
    EventCreate,
    EventResponse,
    PaginatedAttendeesResponse,
    PaginatedEventsResponse,
)
from event_management.api.v1.models.events import Attendee, Event


class EventService:
    @staticmethod
    async def create_event(db, event_data):
        event_dict = event_data.model_dump()
        tz = pytz.timezone("Asia/Kolkata")
        event_obj = Event(**event_dict)
        db.add(event_obj)
        await db.commit()
        await db.refresh(event_obj)
        return event_obj

    @staticmethod
    async def fetch_upcoming_events(
        db: AsyncSession,
        timezone: str = "Asia/Kolkata",
        page: int = 1,
        per_page: int = 10,
    ) -> PaginatedEventsResponse:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        offset = (page - 1) * per_page
        count_result = await db.execute(
            select(func.count()).select_from(
                select(Event).where(Event.start_time > current_time).subquery()
            )
        )
        total_events = count_result.scalar() or 0
        result = await db.execute(
            select(Event)
            .where(Event.start_time > current_time)
            .order_by(Event.start_time)
            .offset(offset)
            .limit(per_page)
        )
        events = result.scalars().all()

        response_events = []
        for event in events:
            count_result = await db.execute(
                select(func.count(Attendee.id)).where(Attendee.event_id == event.id)
            )
            attendee_count = count_result.scalar() or 0
            response_events.append(
                EventResponse(
                    id=event.id,
                    name=event.name,
                    location=event.location,
                    start_time=event.start_time,
                    end_time=event.end_time,
                    max_capacity=event.max_capacity,
                    created_at=event.created_at,
                    updated_at=event.updated_at,
                    attendee_count=attendee_count,
                )
            )
        total_pages = (total_events + per_page - 1) // per_page
        return PaginatedEventsResponse(
            events=response_events,
            total=total_events,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    @staticmethod
    async def register_attendee(
        db: AsyncSession, event_id: int, attendee_data: AttendeeCreate
    ) -> AttendeeResponse:
        """Register an attendee for an event"""
        result = await db.execute(select(Event).where(Event.id == event_id))
        event = result.scalars().first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        tz = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(tz)
        if event.start_time <= current_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot register for past events",
            )
        attendee_obj = await db.execute(
            select(Attendee).where(
                and_(
                    Attendee.event_id == event_id, Attendee.email == attendee_data.email
                )
            )
        )
        attendee_exists = attendee_obj.scalars().first()
        if attendee_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered for this event",
            )
        current_attendees = await db.execute(
            select(func.count(Attendee.id)).where(Attendee.event_id == event_id)
        )
        count = current_attendees.scalars().first()
        if count >= event.max_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event has reached maximum capacity",
            )

        attendee_dict = attendee_data.model_dump()
        attendee = Attendee(event_id=event_id, **attendee_dict)
        db.add(attendee)
        await db.commit()
        await db.refresh(attendee)

        return AttendeeResponse(
            id=attendee.id,
            name=attendee.name,
            email=attendee.email,
            registered_at=attendee.registered_at,
        )

    @staticmethod
    async def fetch_event_attendees(
        db: AsyncSession, event_id: int, page: int = 1, per_page: int = 10
    ) -> PaginatedAttendeesResponse:
        event_obj = await db.execute(select(Event).where(Event.id == event_id))
        event = event_obj.scalars().first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        offset = (page - 1) * per_page

        attendees_obj = await db.execute(
            select(Attendee)
            .where(Attendee.event_id == event_id)
            .order_by(Attendee.registered_at)
            .offset(offset)
            .limit(per_page)
        )
        attendees = attendees_obj.scalars().all()

        count_result = await db.execute(
            select(func.count(Attendee.id)).where(Attendee.event_id == event_id)
        )
        total = count_result.scalar() or 0

        attendee_responses = [
            AttendeeResponse(
                id=attendee.id,
                name=attendee.name,
                email=attendee.email,
                registered_at=attendee.registered_at,
            )
            for attendee in attendees
        ]

        total_pages = math.ceil(total / per_page) if total > 0 else 1

        return PaginatedAttendeesResponse(
            attendees=attendee_responses,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )
