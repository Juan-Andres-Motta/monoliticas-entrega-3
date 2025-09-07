# Tracking Service - Domain-Driven Design with Event-Driven Architecture

A modern tracking service built with FastAPI that implements Domain-Driven Design (DDD) principles and event-driven architecture. The service handles tracking events from marketing campaigns and processes them through different modules using domain events.

## 🏗️ Architecture Overview

This project demonstrates a clean architecture with the following layers:

- **API Layer**: FastAPI routers and schemas
- **Application Layer**: Command handlers and application services
- **Domain Layer**: Aggregates, entities, domain events, and business logic
- **Infrastructure Layer**: Database repositories, external services

### Key Architectural Patterns

- **Domain-Driven Design (DDD)**: Clear separation of concerns with domain aggregates
- **Command Query Responsibility Segregation (CQRS)**: Separate command and query models
- **Event-Driven Architecture**: Modules communicate through domain events
- **Dependency Injection**: Loose coupling through container-based DI

## 🚀 Features

- **Tracking Event Ingestion**: Capture marketing interaction events
- **Domain Event Publishing**: Automatic event publishing when aggregates change
- **Attribution Processing**: Separate module processes events for attribution logic
- **Database Persistence**: SQLAlchemy with SQLite (easily configurable for PostgreSQL)
- **Database Migrations**: Alembic for schema version control
- **Validation**: Business rule enforcement and input validation

## 📋 Project Structure

```
├── api/                           # API Layer
│   ├── routers/                   # FastAPI route handlers
│   └── schemas/                   # Request/Response models
├── ingestion/                     # Ingestion Bounded Context
│   ├── application/               # Application layer
│   │   ├── commands/              # Command DTOs
│   │   └── handlers/              # Command handlers
│   ├── domain/                    # Domain layer
│   │   ├── aggregates/            # Domain aggregates
│   │   ├── events/                # Domain events
│   │   └── repositories/          # Repository interfaces
│   └── infrastructure/            # Infrastructure layer
│       ├── models/                # SQLAlchemy models
│       └── repositories/          # Repository implementations
├── attribution/                   # Attribution Bounded Context
│   └── application/
│       └── handlers/              # Event handlers
├── seedwork/                      # Shared kernel
│   ├── application/               # Base application classes
│   └── domain/                    # Base domain classes
├── config/                        # Configuration
│   ├── container.py               # Dependency injection
│   └── database.py                # Database configuration
└── alembic/                       # Database migrations
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.13+
- Poetry (recommended for dependency management)
- Docker & Docker Compose (optional, for containerized deployment)

### Option 1: Local Development Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd entrega-3

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell

# Or run commands directly with Poetry
poetry run python --version
```

### 2. Database Setup

The project uses SQLite and automatically creates tables when the application starts. You have two options:

**Option A: Automatic Setup (Recommended for development)**
```bash
# Tables are created automatically when you start the server
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Verify database was created
poetry run python check_database.py
```

**Option B: Using Alembic Migrations (For production or schema versioning)**
```bash
# If you want to use migrations instead of auto-creation
poetry run alembic upgrade head

# Verify database setup
poetry run python check_database.py
```

> **Note**: The application is configured to auto-create tables on startup via `Base.metadata.create_all(bind=engine)` in `main.py`. This is convenient for development but you may want to use Alembic migrations for production deployments.

### 3. Start the Server

```bash
# Development mode with auto-reload (using Poetry)
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or simply
poetry run python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/tracking/health

### Option 2: Docker Setup

### 1. Build and Run with Docker

```bash
# Clone the repository
git clone <repository-url>
cd entrega-3

# Build and start the service
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f tracking-service

# Stop the service
docker-compose down
```

### 2. Docker Commands

```bash
# Build the image
docker-compose build

# Start the service
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop and remove containers
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

The containerized API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs  
- **Health Check**: http://localhost:8000/api/v1/tracking/health

> **Note**: The SQLite database will be persisted in the `./data` directory on your host machine.

## 📝 API Usage

### Record a Tracking Event

```bash
POST /api/v1/tracking/events
Content-Type: application/json

{
  "partner_id": "google-ads",
  "campaign_id": "summer-sale-2025",
  "visitor_id": "user123",
  "interaction_type": "click",
  "source_url": "https://google.com/ad",
  "destination_url": "https://mystore.com/products"
}
```

**Valid interaction types**: `click`, `view`, `engagement`

### Example Response

```json
{
  "tracking_event_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "recorded",
  "message": "Tracking event recorded successfully",
  "processing_time_ms": 45.2
}
```

## 🔄 Domain Events Flow

1. **Event Creation**: When a tracking event is recorded, a `TrackingEventRecorded` domain event is created
2. **Event Publishing**: After successful persistence, the domain event is published
3. **Event Processing**: The Attribution module receives and processes the event
4. **Attribution Logic**: Calculates attribution metrics based on interaction type

```mermaid
graph LR
    A[API Request] --> B[Command Handler]
    B --> C[Domain Aggregate]
    C --> D[Repository Save]
    D --> E[Publish Domain Event]
    E --> F[Attribution Handler]
    F --> G[Attribution Processing]
```

## 🧪 Testing

### Manual Testing

```bash
# Test the API endpoints
curl -X POST "http://localhost:8000/api/v1/tracking/events" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_id": "google-ads",
    "campaign_id": "summer-sale-2025", 
    "visitor_id": "user123",
    "interaction_type": "click",
    "source_url": "https://google.com/ad",
    "destination_url": "https://mystore.com/products"
  }'

# Check database contents
poetry run python check_database.py

# Test domain events (requires aiohttp)
poetry add aiohttp --group dev  # Add aiohttp for testing
poetry run python test_domain_events.py
```

### Using the Interactive Documentation

Visit http://localhost:8000/docs to use the Swagger UI for testing the API interactively.

## 🗄️ Database

The project uses SQLite by default for development. The database file `tracking_service.db` will be created automatically when you first start the server.

### Automatic Table Creation

The application is configured to automatically create database tables on startup using SQLAlchemy's `Base.metadata.create_all()`. This means:

- **No manual setup required** - just start the server
- **Database file created automatically** in the project root
- **Tables created from SQLAlchemy models** on first run

### Database Schema

```sql
CREATE TABLE tracking_events (
    tracking_event_id UUID PRIMARY KEY,
    partner_id VARCHAR(255) NOT NULL,
    campaign_id VARCHAR(255) NOT NULL, 
    visitor_id VARCHAR(255) NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,
    source_url TEXT NOT NULL,
    destination_url TEXT NOT NULL,
    recorded_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Migration Commands (Optional)

Alembic is configured but not required since tables are auto-created. Use these commands if you want to manage schema changes with migrations:

```bash
# Create a new migration (only if you want to use migrations)
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations (alternative to auto-creation)
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1
```

> **Note**: You can disable auto-creation by removing `Base.metadata.create_all(bind=engine)` from `main.py` if you prefer to use only Alembic migrations.

## ⚙️ Configuration

### Database Configuration

Edit `config/database.py` or set environment variable:

```bash
# For PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost:5432/tracking_db"

# For MySQL
export DATABASE_URL="mysql://user:password@localhost:3306/tracking_db"
```

### Adding New Event Handlers

1. Create a new handler class inheriting from `DomainEventHandler`
2. Register it in `config/container.py`:

```python
# In _setup_dependencies method
new_handler = YourEventHandler()
event_publisher.register_handler("tracking_event.recorded.v1", new_handler)
```

## 🚦 Health Monitoring

- **Health Check**: `GET /api/v1/tracking/health`
- **Server Logs**: Monitor console output for domain event processing
- **Database Check**: Use `poetry run python check_database.py` to verify data persistence

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add tests for new features
3. Update database migrations when changing models
4. Document any new configuration options

## 📚 Key Concepts Demonstrated

- **Aggregate Root**: `TrackingEvent` as the main domain aggregate
- **Domain Events**: `TrackingEventRecorded` published when state changes
- **Repository Pattern**: Abstract repository with concrete implementations
- **Command Handler**: Processes commands and coordinates domain logic
- **Event Publisher**: Decouples modules through asynchronous event processing
- **Dependency Injection**: Clean separation of concerns through DI container

This project serves as a practical example of implementing modern software architecture patterns in Python with FastAPI.
