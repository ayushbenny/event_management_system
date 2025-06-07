import pytest
from datetime import datetime, timedelta
from event_management.api.v1.schemas.events import EventCreate, AttendeeCreate
from event_management.api.v1.models.events import Event
from event_management.views import EventService


@pytest.mark.asyncio
async def test_create_event(async_session):
    event_data = EventCreate(
        name="Test Event",
        location="Test Location",
        start_time=datetime.now() + timedelta(hours=1),
        end_time=datetime.now() + timedelta(hours=2),
        max_capacity=100,
    )
    event = await EventService.create_event(async_session, event_data)
    assert event.name == "Test Event"


@pytest.mark.asyncio
async def test_fetch_upcoming_events(async_session):
    event_data = EventCreate(
        name="Upcoming Event",
        location="Delhi",
        start_time=datetime.now() + timedelta(hours=1),
        end_time=datetime.now() + timedelta(hours=2),
        max_capacity=10,
    )
    await EventService.create_event(async_session, event_data)

    response = await EventService.fetch_upcoming_events(async_session)
    assert response.total >= 1
    assert isinstance(response.events[0].name, str)


@pytest.mark.asyncio
async def test_register_attendee(async_session):
    event_data = EventCreate(
        name="Register Test Event",
        location="Karnataka",
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=3),
        max_capacity=1,
    )
    event = await EventService.create_event(async_session, event_data)

    attendee_data = AttendeeCreate(
        name="Ayush Benny",
        email="ayushbenny@gmail.com",
    )
    response = await EventService.register_attendee(
        async_session, event.id, attendee_data
    )
    assert response.name == "Ayush Benny"
    assert response.email == "ayushbenny@gmail.com"


@pytest.mark.asyncio
async def test_register_attendee_duplicate_email(async_session):
    event_data = EventCreate(
        name="Duplicate Email Event",
        location="Bangalore",
        start_time=datetime.now() + timedelta(hours=3),
        end_time=datetime.now() + timedelta(hours=4),
        max_capacity=2,
    )
    event = await EventService.create_event(async_session, event_data)

    attendee_data = AttendeeCreate(name="Pooja", email="pooja@gmail.com")
    await EventService.register_attendee(async_session, event.id, attendee_data)

    with pytest.raises(Exception) as exc:
        await EventService.register_attendee(async_session, event.id, attendee_data)
    assert "already registered" in str(exc.value)


@pytest.mark.asyncio
async def test_register_attendee_capacity_reached(async_session):
    event_data = EventCreate(
        name="Full Capacity Event",
        location="Kerala",
        start_time=datetime.now() + timedelta(hours=3),
        end_time=datetime.now() + timedelta(hours=4),
        max_capacity=1,
    )
    event = await EventService.create_event(async_session, event_data)

    await EventService.register_attendee(
        async_session, event.id, AttendeeCreate(name="Sagarika", email="sagarika@gmail.com")
    )

    with pytest.raises(Exception) as exc:
        await EventService.register_attendee(
            async_session,
            event.id,
            AttendeeCreate(name="Asif", email="asif@gmail.com"),
        )
    assert "maximum capacity" in str(exc.value)


@pytest.mark.asyncio
async def test_fetch_event_attendees(async_session):
    event_data = EventCreate(
        name="Attendee List Event",
        location="Hyderabad",
        start_time=datetime.now() + timedelta(hours=5),
        end_time=datetime.now() + timedelta(hours=6),
        max_capacity=10,
    )
    event = await EventService.create_event(async_session, event_data)

    await EventService.register_attendee(
        async_session, event.id, AttendeeCreate(name="Arjun", email="arjun@gmail.com")
    )
    await EventService.register_attendee(
        async_session, event.id, AttendeeCreate(name="Sudheer", email="sudheer@gmail.com")
    )

    attendees = await EventService.fetch_event_attendees(async_session, event.id)
    assert attendees.total == 2
    assert attendees.attendees[0].email == "arjun@gmail.com"
