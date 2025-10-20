
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User question or message")
    session_id: str | None = Field(None, description="Optional session ID for conversation history")

class ChatResponse(BaseModel):
    message: str = Field(..., description="AI response message chunk")
    done: bool = Field(False, description="Whether the full response is completed")
