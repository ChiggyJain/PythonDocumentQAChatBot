import io
import pytest
import pathlib
from fastapi.testclient import TestClient
from main import app
from backend.api.v1.agents.chatbot_agents import ChatBotAgent
    
client = TestClient(app)
chatBotAgentManager = ChatBotAgent()


# Chat Ask Routes

def test_chat_ask_without_pdf():
    """Test normal conversation when no PDF uploaded."""
    payload = {
        "userId": "11",
        "userSessionId": "111",
        "prompt": "Hello, how are you?"
    }
    response = client.post("/api/v1/chat/ask", json=payload)
    print(f"test_chat_ask_without_pdf func Response: {response.text}\n")
    assert response.status_code == 200 or response.status_code == 206
    

def test_chat_ask_with_pdf_context():
    """Test QA-based chat when PDF is uploaded."""
    userId = "11"
    userSessionId = "111"
    agentInstancesDict = chatBotAgentManager.get_or_create_agent(userId, userSessionId)
    agentInstancesDict['all_pdf_text'].append("The Eiffel Tower is located in Paris, France.")
    agentInstancesDict['overall_pdf_text']+= "\n" + "The Eiffel Tower is located in Paris, France."
    payload = {
        "userId": userId,
        "userSessionId": userSessionId,
        "prompt": "Where is the Eiffel Tower located?"
    }
    response = client.post("/api/v1/chat/ask", json=payload)
    print(f"test_chat_ask_without_pdf func Response: {response.text}\n")
    assert response.status_code == 200 or response.status_code == 206



def test_chat_session_history():
    """Fetch chat session history."""
    params = {"userId": "11", "userSessionId": "111"}
    response = client.get("/api/v1/chat/chat_session_history", params=params)
    result = response.json()
    print(f"test_chat_session_history func Response: {result}\n")
    assert response.status_code == 200
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result


def test_reset_chat_session_history():
    """Reset chat session history."""
    params = {"userId": "11", "userSessionId": "111"}
    response = client.post("/api/v1/chat/reset_chat_session_history", json=params)
    result = response.json()
    print(f"test_reset_chat_session_history func Response: {result}\n")
    assert response.status_code == 200
    assert "status_code" in result
    assert "messages" in result
    assert "data" in result        