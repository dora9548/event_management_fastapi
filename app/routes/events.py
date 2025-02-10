from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter()

@router.post("/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    return crud.create_event(db, event)

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(database.get_db)):
    db_event = crud.update_event(db, event_id, event)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event
