
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")
    prompt: str = Field(..., description="User Question or Message")


class ChatHistoryRequest(BaseModel):
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")

class ChatHistoryResetRequest(BaseModel):
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")
