from sqlalchemy.orm import Session
from app import models, schemas

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if db_event:
        for key, value in event_update.dict().items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def register_attendee(db: Session, attendee: schemas.AttendeeCreate):
    event = db.query(models.Event).filter(models.Event.event_id == attendee.event_id).first()
    if not event or len(event.attendees) >= event.max_attendees:
        return None
    db_attendee = models.Attendee(**attendee.dict())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

def check_in_attendee(db: Session, attendee_id: int):
    attendee = db.query(models.Attendee).filter(models.Attendee.attendee_id == attendee_id).first()
    if attendee:
        attendee.check_in_status = True
        db.commit()
        db.refresh(attendee)
    return attendee
