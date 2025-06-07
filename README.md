# 📅 Event Management Service

A event management REST API built with FastAPI, SQLAlchemy, and PostgreSQL. This service allows users to create events, register attendees, and manage event data with timezone-aware filtering and pagination.

## 🚀 Features

- **Event Management**: Create and list upcoming events
- **Attendee Registration**: Register attendees to events with email validation
- **Pagination Support**: Paginated APIs for both events and attendees
- **Timezone Awareness**: Event filtering with timezone support
- **Data Integrity**: Email uniqueness constraint per event
- **Auto-generated Documentation**: Interactive API docs with Swagger UI

## 📦 Technology Stack

- **Backend**: Python 3.10+, FastAPI
- **Database**: PostgreSQL with SQLAlchemy (Async)
- **Validation**: Pydantic models
- **Migrations**: Alembic (optional)
- **Server**: Uvicorn (ASGI server)

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/event-management.git
cd event-management
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Configuration

Configure your database connection in `common/database.py` or use environment variables:

```python
DATABASE_URL = "postgresql+asyncpg://<username>:<password>@<host>:<port>/<db_name>"
```

For environment management, create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<db_name>
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 🧠 Key Assumptions

- **Default Timezone**: "Asia/Kolkata" (can be overridden via query parameters)
- **Email Uniqueness**: One attendee can register only once per event
- **Authentication**: No authentication required (simplified for demo purposes)

## 📬 API Endpoints

### ✅ Health Check

```bash
curl http://localhost:8000/event/v1/health_check
```

**Response:**

```json
{
  "status": "active",
  "message": "Event Management Service is up and running"
}
```

### 📌 Create Event

```bash
curl -X POST http://localhost:8000/event/v1/create_events \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Conference 2025",
    "location": "Bangalore",
    "start_time": "2025-07-20",
    "end_time": "2025-07-21",
    "max_capacity": 100
  }'
```

**Response:**

```json
{
  "id": 1,
  "name": "Tech Conference 2025",
  "location": "Bangalore",
  "start_time": "2025-07-20",
  "end_time": "2025-07-21",
  "max_capacity": 100,
  "registered_count": 0
}
```

### 📅 Fetch Upcoming Events

```bash
curl "http://localhost:8000/event/v1/events?page=1&per_page=5"
```

**Query Parameters:**

- `timezone` (optional): Timezone for filtering (default: "Asia/Kolkata")
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10, max: 100)

**Response:**

```json
{
  "events": [
    {
      "id": 1,
      "name": "Tech Conference 2025",
      "location": "Bangalore",
      "start_time": "2025-07-20T10:00:00+05:30",
      "end_time": "2025-07-20T17:00:00+05:30",
      "max_capacity": 100,
      "registered_count": 25
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 5,
  "pages": 1
}
```

### 🧾 Register Attendee

```bash
curl -X POST http://localhost:8000/event/v1/<event_id>/register_attendee \
  -H "Content-Type: application/json" \
  -d '{
  "name": "John Dcruz",
  "email": "john.dcruz@example.com"
}'
```

**Response:**

```json
{
  "name": "John Dcruz",
  "email": "john.dcruz@example.com",
  "id": 20,
  "registered_at": "2025-06-07T06:32:32.979206Z"
}
```

### 👥 Fetch Event Attendees

```bash
curl "http://localhost:8000/event/v1/4/attendees?page=1&per_page=10"
```

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `per_page` (optional): Items per page (default: 10, max: 100)

**Response:**

```json
{
  "attendees": [
    {
      "name": "John Dcruz",
      "email": "john.dcruz@example.com",
      "id": 20,
      "registered_at": "2025-06-07T06:32:32.979206Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "pages": 1
}
```

## 🧪 Testing

### Interactive API Documentation

Visit the auto-generated Swagger UI documentation:

```
http://localhost:8000/docs
```

### Alternative Documentation

ReDoc format is also available:

```
http://localhost:8000/redoc
```

### Using Postman

1. Import the provided curl commands
2. Set up environment variables for base URL
3. Test all endpoints with different scenarios

### Manual Testing Scenarios

1. **Create multiple events** with different timezones
2. **Register attendees** and verify email uniqueness
3. **Test pagination** with large datasets
4. **Verify timezone filtering** with different timezone parameters
5. **Test capacity limits** by registering maximum attendees

## 🔧 Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations (Optional)

If using Alembic for migrations:

```bash
# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```
