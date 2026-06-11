from sqlalchemy.orm import Session

from app.models import WebhookEvent


def get_event_by_event_id(db: Session, event_id: str):
    return (
        db.query(WebhookEvent)
        .filter(WebhookEvent.event_id == event_id)
        .first()
    )


def create_event(db: Session, event: WebhookEvent):
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, event: WebhookEvent):
    db.commit()
    db.refresh(event)
    return event


def get_events(db: Session, status=None, limit=10, offset=0):
    query = db.query(WebhookEvent)

    if status:
        query = query.filter(WebhookEvent.status == status)

    return query.offset(offset).limit(limit).all()