from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import WebhookCreate, WebhookResponse
from app.services import create_webhook, retry_webhook
from app.models import WebhookEvent

router = APIRouter()


@router.post("/webhooks")
def create(data: WebhookCreate, db: Session = Depends(get_db)):
    event = create_webhook(db, data)

    if event is None:
        return {"message": "Duplicate ignored"}

    return event


@router.get("/webhooks", response_model=list[WebhookResponse])
def get_webhooks(
    status: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):

    query = db.query(WebhookEvent)

    if status:
        query = query.filter(WebhookEvent.status == status)

    return query.offset(offset).limit(limit).all()


@router.post("/webhooks/{event_id}/retry")
def retry(event_id: str, db: Session = Depends(get_db)):

    result = retry_webhook(db, event_id)

    if result == "not_found":
        raise HTTPException(status_code=404, detail="Webhook not found")

    if result == "already_processed":
        return {"message": "Already processed"}

    return result