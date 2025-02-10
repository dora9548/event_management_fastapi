from fastapi import FastAPI
from app.database import engine, Base
from app.routes import events, attendees
from app.auth import oauth2_scheme

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Event Management API", description="An API for managing events and attendees.", version="1.0.0")

# Include Routers
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(attendees.router, prefix="/attendees", tags=["Attendees"])

@app.get("/")
def root():
    return {"message": "Welcome to the Event Management API"}
