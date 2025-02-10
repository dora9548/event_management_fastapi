from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from app import schemas, crud, database

router = APIRouter()

@router.post("/", response_model=schemas.AttendeeResponse)
def register_attendee(attendee: schemas.AttendeeCreate, db: Session = Depends(database.get_db)):
    db_attendee = crud.register_attendee(db, attendee)
    if not db_attendee:
        raise HTTPException(status_code=400, detail="Event is full or does not exist")
    return db_attendee

@router.put("/{attendee_id}/check-in", response_model=schemas.AttendeeResponse)
def check_in_attendee(attendee_id: int, db: Session = Depends(database.get_db)):
    db_attendee = crud.check_in_attendee(db, attendee_id)
    if not db_attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return db_attendee

@router.get("/event/{event_id}", response_model=List[schemas.AttendeeResponse])
def list_attendees(event_id: int, db: Session = Depends(database.get_db)):
    attendees = db.query(database.models.Attendee).filter(database.models.Attendee.event_id == event_id).all()
    return attendees

@router.post("/bulk-check-in")
def bulk_check_in(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    df = pd.read_csv(file.file)
    if "attendee_id" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'attendee_id' column")
    
    check_in_count = 0
    for attendee_id in df["attendee_id"]:
        attendee = crud.check_in_attendee(db, attendee_id)
        if attendee:
            check_in_count += 1
    
    return {"message": f"Bulk check-in completed for {check_in_count} attendees"}
