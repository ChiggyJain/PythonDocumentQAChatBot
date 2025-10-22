

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., description="Enter your account username")
    password: str = Field(..., description="Enter your account password")