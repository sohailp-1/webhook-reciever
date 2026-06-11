from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class WebhookCreate(BaseModel):
    event_id: str
    event_type: str
    payload: Dict[str, Any]


class WebhookResponse(BaseModel):
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    status: str
    attempts: int
    last_error: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }