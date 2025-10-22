
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User Question or Message")
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")

class ChatResponse(BaseModel):
    message: str = Field(..., description="AI response message chunk")
    done: bool = Field(False, description="Whether the full response is completed")
