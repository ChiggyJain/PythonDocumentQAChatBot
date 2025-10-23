


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import io
import pytest
import pathlib
from fastapi.testclient import TestClient
from main import app
from backend.api.v1.agents.chatbot_agents import ChatBotAgent
    
client = TestClient(app)
chatBotAgentManager = ChatBotAgent()


# Upload Pdf File Routes

def test_upload_pdf_success():
    """Test uploading an existing PDF file from disk."""
    pdf_path = pathlib.Path(__file__).parent.parent/"data/SampleFileLessThan5MB.pdf"
    with open(pdf_path, "rb") as f:
        files = {"file": (pdf_path.name, f, "application/pdf")}
        data = {"userId": "11", "userSessionId": "111"}
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
    result = response.json()
    print(f"test_upload_pdf_success func Response: {result}\n")
    assert response.status_code == 200
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result


def test_upload_non_pdf_success():
    """Test uploading an existing PDF file from disk."""
    pdf_path = pathlib.Path(__file__).parent.parent/"data/SampleTextFile.txt"
    with open(pdf_path, "rb") as f:
        files = {"file": (pdf_path.name, f, "application/pdf")}
        data = {"userId": "11", "userSessionId": "111"}
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
    result = response.json()
    print(f"test_upload_non_pdf_success func Response: {result}\n")
    assert response.status_code == 400
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result


def test_upload_pdf_empty_success():
    """Test uploading an existing PDF file from disk."""
    pdf_path = pathlib.Path(__file__).parent.parent/"data/SampleBlankFile.pdf"
    with open(pdf_path, "rb") as f:
        files = {"file": (pdf_path.name, f, "application/pdf")}
        data = {"userId": "11", "userSessionId": "111"}
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
    result = response.json()
    print(f"test_upload_pdf_empty_success func Response: {result}\n")
    assert response.status_code == 400
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result


def test_upload_pdf_larger_success():
    """Test uploading an existing PDF file from disk."""
    pdf_path = pathlib.Path(__file__).parent.parent/"data/SampleFileGreaterThan5MB.pdf"
    with open(pdf_path, "rb") as f:
        files = {"file": (pdf_path.name, f, "application/pdf")}
        data = {"userId": "11", "userSessionId": "111"}
        response = client.post("/api/v1/pdf/upload", files=files, data=data)
    result = response.json()
    print(f"test_upload_pdf_larger_success func Response: {result}\n")
    assert response.status_code == 400
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result

