

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from typing import AsyncGenerator
from backend.api.v1.schemas.chat_schema import *
from backend.api.v1.agents.chatbot_agents import ChatBotAgent
from backend.api.v1.utils.utils import *

router = APIRouter()
chatBotAgentManager = ChatBotAgent()
# print(f"chat-routes-chatBotAgentManager-instances-id: {id(chatBotAgentManager)}\n")





async def generate_response_tokens(prompt: str, userId:str, userSessionId:str) -> AsyncGenerator[str, None]:
    """
    Calls the AI agent asynchronously and yields tokens one by one.
    """
    try:
        async for token in chatBotAgentManager.get_response(prompt=prompt, userId=userId, userSessionId=userSessionId):
            yield token
        yield f"data: [STREAM_COMPLETED]"
    except Exception as e:
        error_rsp = standard_response(
            status_code=500,
            messages=[f"[ERROR] generate_response_tokens AI Agent failed: {str(e)}"],
            data=None
        )
        # yield formatted JSON so frontend can handle it
        yield f"data: {error_rsp}"



@router.post("/ask", response_class=StreamingResponse, status_code=status.HTTP_200_OK, summary="User ask a question and return streaming response as token-by-token")
async def ask_chat(chat_request: ChatRequest):
    """
    Stream AI response token-by-token for a user prompt.
    - userId: Enter loggedIn user userId
    - userSessionId: Enter loggedIn user userSessionId
    - prompt: Enter prompt message/question
    """
    # print(f"chat_request: {chat_request}\n")
    userId = chat_request.userId
    userSessionId = chat_request.userSessionId
    prompt = chat_request.prompt
    # Token generator function for StreamingResponse
    async def event_stream():
        async for token in generate_response_tokens(prompt=prompt, userId=userId, userSessionId=userSessionId):
            # print(f"event_stream Token: {token}\n")
            yield f"data: {token}\n\n"
    return StreamingResponse(content=event_stream(), media_type="text/event-stream")



@router.get("/history/{session_id}", response_model=list[ChatHistoryResponse], summary="Chat History Details for Respective User-ID and User-Session-ID")
async def get_chat_history(session_id: str):
    """
    Retrieve full chat session history for a given session_id
    """
    try:
        history = chatBotAgentManager.get_history(session_id)
        response_list = [ChatHistoryResponse(message=msg, done=True) for msg in history]
        return response_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve chat history: {str(e)}")

