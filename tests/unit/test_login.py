

import pytest
from fastapi.testclient import TestClient
from main import app
    
client = TestClient(app)


# Login Routes

def test_authenticate_user_login_success():
    """Test valid user login."""
    payload = {"username": "admin1", "password": "admin2"}
    response = client.post("/api/v1/login/authenticate_login_user", json=payload)
    result = response.json()
    print(f"test_authenticate_user_login_success func Response: {result}\n")
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result
    assert result["status_code"] == 200
    assert result["data"]['userId'] == "11"


def test_authenticate_user_login_failure():
    """Test valid user login."""
    payload = {"username": "admin4", "password": "admin4"}
    response = client.post("/api/v1/login/authenticate_login_user", json=payload)
    result = response.json()
    print(f"test_authenticate_user_login_failure func Response: {result}\n")
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result
    assert result["status_code"] == 401

