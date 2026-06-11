from sqlalchemy.orm import Session

from app.models import WebhookEvent
from app.schemas import WebhookCreate


def process_event(event: WebhookEvent):
    """
    Process a webhook event.
    """

    event.attempts += 1

    # Retry success condition
    if event.payload.get("force_success") is True:
        event.status = "processed"
        event.last_error = None
        return

    # Failure condition
    if "fail" in event.event_type.lower():
        event.status = "failed"
        event.last_error = "Processing failed"
    else:
        event.status = "processed"
        event.last_error = None


def create_webhook(db: Session, webhook: WebhookCreate):
    """
    Create a new webhook if it doesn't already exist.
    """

    existing_event = (
        db.query(WebhookEvent)
        .filter(WebhookEvent.event_id == webhook.event_id)
        .first()
    )

    if existing_event:
        return None

    event = WebhookEvent(
        event_id=webhook.event_id,
        event_type=webhook.event_type,
        payload=webhook.payload,
        status="received",
        attempts=0,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    process_event(event)

    db.commit()
    db.refresh(event)

    return event


def retry_webhook(db: Session, event_id: str):

    event = (
        db.query(WebhookEvent)
        .filter(WebhookEvent.event_id == event_id)
        .first()
    )

    if not event:
        return "not_found"

    if event.status == "processed":
        return "already_processed"

    process_event(event)

    db.commit()
    db.refresh(event)

    return event