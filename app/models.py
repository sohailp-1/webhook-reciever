from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

from app.database import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(String, unique=True, nullable=False, index=True)

    event_type = Column(String, nullable=False)

    payload = Column(JSON, nullable=False)

    status = Column(String, default="received")

    attempts = Column(Integer, default=0)

    last_error = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )