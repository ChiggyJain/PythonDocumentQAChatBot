

from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from typing import AsyncGenerator
import json
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
            messages=[f"Error occured in generate_response_tokens func: {str(e)}"],
            data={}
        )
        # yield formatted JSON so frontend can handle it
        yield f"data: {json.dumps(error_rsp)}"



@router.post("/ask", response_class=StreamingResponse, status_code=status.HTTP_200_OK, summary="User ask a question and return streaming response as token-by-token")
async def ask_chat(chat_request: ChatRequest):
    """
    Stream AI response token-by-token for a user prompt.
    - userId: Enter loggedIn user userId
    - userSessionId: Enter loggedIn user userSessionId
    - prompt: Enter prompt message/question
    """
    try:
        # print(f"chat_request: {chat_request}\n")
        userId = chat_request.userId
        userSessionId = chat_request.userSessionId
        prompt = chat_request.prompt
        async def event_stream():
            async for token in generate_response_tokens(prompt=prompt, userId=userId, userSessionId=userSessionId):
                # print(f"event_stream Token: {token}\n")
                yield f"data: {token}\n\n"
        return StreamingResponse(content=event_stream(), media_type="text/event-stream")
    except Exception as e:
        error_rsp = standard_response(
            status_code=500,
            messages=[f"Error occured in ask_chat func: {str(e)}"],
            data={}
        )
        return StreamingResponse(content=f"data: {json.dumps(error_rsp)}", media_type="text/event-stream")



@router.get("/chat_history/", summary="Chat History Details for Respective User-ID and User-Session-ID")
async def get_chat_history(chat_history_request:ChatHistoryRequest = Depends()):
    """
    Retrieve full chat history messages
    - userId: Enter loggedIn user userId
    - userSessionId: Enter loggedIn user userSessionId
    """
    chatHistoryRspObj = standard_response(status_code=400, messages=["No chat history found"], data={})
    try:
        # print(f"chat_history_request: {chat_history_request}\n")
        userId = chat_history_request.userId
        userSessionId = chat_history_request.userSessionId
        chatHistoryRspObj = chatBotAgentManager.get_history(userId, userSessionId)
    except Exception as e:
        chatHistoryRspObj['status_code'] = 500
        chatHistoryRspObj['messages'] = [f"Error occured while retrieving chat history: {str(e)}"]
    return JSONResponse(
        status_code=chatHistoryRspObj['status_code'],
        content=chatHistoryRspObj
    )


@router.post("/reset_chat_history/", summary="Reset Chat History Details for Respective User-ID and User-Session-ID")
async def reset_chat_history(chat_history_reset_request:ChatHistoryResetRequest):
    """
    Reset chat history messages
    - userId: Enter loggedIn user userId
    - userSessionId: Enter loggedIn user userSessionId
    """
    resetChatHistoryRspObj = standard_response(status_code=400, messages=["Chat history is not reset"], data={})
    try:
        # print(f"chat_history_request: {chat_history_request}\n")
        userId = chat_history_reset_request.userId
        userSessionId = chat_history_reset_request.userSessionId
        resetChatHistoryRspObj = chatBotAgentManager.reset_chat_history(userId, userSessionId)
    except Exception as e:
        resetChatHistoryRspObj['status_code'] = 500
        resetChatHistoryRspObj['messages'] = [f"Error occured while reset chat history: {str(e)}"]
    return JSONResponse(
        status_code=resetChatHistoryRspObj['status_code'],
        content=resetChatHistoryRspObj
    )

