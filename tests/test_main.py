from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/events/", json={"name": "Tech Summit", "start_time": "2025-04-10T10:00:00", "end_time": "2025-04-10T18:00:00", "location": "New York", "max_attendees": 100})
    assert response.status_code == 200
