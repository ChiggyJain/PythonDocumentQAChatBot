
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")
    prompt: str = Field(..., description="User Question or Message")


class ChatSessionHistoryRequest(BaseModel):
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")

class ChatSessionHistoryResetRequest(BaseModel):
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")
