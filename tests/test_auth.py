from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_login():

    email = f"test_{uuid.uuid4()}@test.com"

    # register user
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "123456"
        }
    )

    # login
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    assert response.status_code == 200