

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from backend.api.v1.schemas.chat_schema import *
from backend.api.v1.agents.chatbot_agents import ChatBotAgent
from typing import AsyncGenerator

router = APIRouter()
chat_agent = ChatBotAgent()






async def generate_response_tokens(prompt: str, session_id: str | None = None) -> AsyncGenerator[str, None]:
    
    """
    Calls the AI agent asynchronously and yields tokens one by one.
    """

    try:
        async for token in chat_agent.get_response(prompt=prompt, session_id=session_id):
            yield token
    except Exception as e:
        yield f"[ERROR] generate_response_tokens AI Agent failed: {str(e)}"



@router.post("/ask", response_class=StreamingResponse, status_code=status.HTTP_200_OK)
async def ask_chat(chat_request: ChatRequest):

    """
    Stream AI response token-by-token for a user prompt.
    Example request:
    {
        "prompt": "Who is Albert Einstein?",
        "session_id": "123abc"
    }
    """

    print(f"chat_request: {chat_request}\n")

    prompt = chat_request.prompt
    session_id = chat_request.session_id

    if not prompt or prompt.strip() == "":
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    # Token generator function for StreamingResponse
    async def event_stream():
        async for token in generate_response_tokens(prompt=prompt, session_id=session_id):
            # Yield tokens as Server-Sent Events (SSE)
            # print(f"event_stream Token: {token}\n")
            yield f"data: {token}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")



@router.get("/history/{session_id}", response_model=list[ChatResponse])
async def get_chat_history(session_id: str):

    """
    Retrieve full chat session history for a given session_id
    """

    try:
        history = chat_agent.get_history(session_id)
        response_list = [ChatResponse(message=msg, done=True) for msg in history]
        return response_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chat history: {str(e)}")

