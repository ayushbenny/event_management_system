from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from common.database import get_db
from event_management import views
from event_management.api.v1.schemas.events import (
    AttendeeCreate,
    AttendeeResponse,
    EventCreate,
    EventResponse,
    PaginatedAttendeesResponse,
    PaginatedEventsResponse,
)

event_management_router = APIRouter()


@event_management_router.get("/health_check")
async def health_check():
    """
    Health check endpoint to verify if the Event Management Service is running.

    Returns:
        dict: A status message indicating the service is active.
    """
    return {"status": "active", "message": "Event Management Service is up and running"}


@event_management_router.post(
    "/create_events", response_model=EventResponse, status_code=status.HTTP_201_CREATED
)
async def create_event(event_data: EventCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new event.

    Args:
        event_data (EventCreate): The data required to create a new event.
        db (AsyncSession, optional): Async database session dependency.

    Returns:
        EventResponse: Details of the newly created event.

    Raises:
        HTTPException: If event creation fails due to validation or database errors.
    """
    return await views.EventService.create_event(db, event_data)


@event_management_router.get("/events", response_model=PaginatedEventsResponse)
async def fetch_upcoming_events(
    timezone: str = Query(
        "Asia/Kolkata", description="Timezone for filtering upcoming events"
    ),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch a paginated list of upcoming events filtered by timezone.

    Args:
        timezone (str, optional): Timezone to filter events. Defaults to "Asia/Kolkata".
        page (int, optional): Page number for pagination. Defaults to 1.
        per_page (int, optional): Number of events per page (max 100). Defaults to 10.
        db (AsyncSession, optional): Async database session dependency.

    Returns:
        PaginatedEventsResponse: Paginated list of upcoming events.
    """
    return await views.EventService.fetch_upcoming_events(db, timezone, page, per_page)


@event_management_router.post(
    "/{event_id}/register_attendee",
    response_model=AttendeeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_attendee(
    event_id: int, attendee_data: AttendeeCreate, db: AsyncSession = Depends(get_db)
):
    """
    Register a new attendee for a specific event.

    Args:
        event_id (int): The ID of the event to register for.
        attendee_data (AttendeeCreate): The data of the attendee to register.
        db (AsyncSession, optional): Async database session dependency.

    Returns:
        AttendeeResponse: Details of the registered attendee.

    Raises:
        HTTPException: If the event does not exist or registration fails.
    """
    return await views.EventService.register_attendee(db, event_id, attendee_data)


@event_management_router.get(
    "/{event_id}/attendees", response_model=PaginatedAttendeesResponse
)
async def fetch_event_attendees(
    event_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch a paginated list of attendees for a specific event.

    Args:
        event_id (int): The ID of the event whose attendees are to be fetched.
        page (int, optional): Page number for pagination. Defaults to 1.
        per_page (int, optional): Number of attendees per page (max 100). Defaults to 10.
        db (AsyncSession, optional): Async database session dependency.

    Returns:
        PaginatedAttendeesResponse: Paginated list of attendees for the event.

    Raises:
        HTTPException: If the event does not exist.
    """
    return await views.EventService.fetch_event_attendees(db, event_id, page, per_page)
