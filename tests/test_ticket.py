from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_ticket():

    email = f"ticket_{uuid.uuid4()}@test.com"

    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "123456"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/tickets",
        data={
            "title": "Test Ticket",
            "description": "Testing ticket",
            "priority": "medium"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200