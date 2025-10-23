
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# System Health Routes

def test_system_health_check_success():
    """Verify backend system health route."""
    response = client.get("/api/v1/system/system-health")
    result = response.json()
    print(f"test_system_health_check_success func Response: {result}\n")
    assert "status_code" in result
    assert "messages" in result
    assert result["status_code"] == 200
    assert result["messages"][0] == "Document-QA-ChatBot Backend System is Up & Running"


def test_system_health_check_failure():
    """Verify backend system health route."""
    response = client.get("/api/v1/system/system-health")
    result = response.json()
    print(f"test_system_health_check_failure func Response: {result}\n")
    assert "status_code" in result
    assert "messages" in result
    assert result["status_code"] == 200
    assert result["messages"][0] == "Document-QA-ChatBot Backend System is Up & Running"

