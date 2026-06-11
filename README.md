Webhook Receiver + Retry Service

Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- Poetry
- Pytest

Installation

poetry install

Run

poetry run uvicorn app.main:app --reload

API Endpoints

POST /webhooks
GET /webhooks
POST /webhooks/{event_id}/retry

Run Tests

pytest