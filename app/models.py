from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class EventStatus(str, enum.Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    canceled = "canceled"

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    max_attendees = Column(Integer, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.scheduled)

    attendees = relationship("Attendee", back_populates="event")

class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False) 
    last_name = Column(String(100), nullable=False)   
    email = Column(String(255), unique=True, nullable=False)  
    phone_number = Column(String(15), unique=True, nullable=False)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    check_in_status = Column(Boolean, default=False)

    event = relationship("Event", back_populates="attendees")

