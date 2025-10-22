

from fastapi import APIRouter, UploadFile, File, Form, status
from pydantic import BaseModel, Field


class UploadPdfFileRequest(BaseModel):
    userId: str = Field(..., description="LoggedIn User-ID")
    userSessionId: str = Field(..., description="LoggedIn User Chat-Session-ID")
    file: UploadFile = Field(..., description="PDF file to upload")

    @classmethod
    def as_form(
        cls,
        userId: str = Form(...),
        userSessionId: str = Form(...),
        file: UploadFile = File(...)
    ):
        """Helper to let FastAPI parse multipart form into Pydantic model"""
        return cls(userId=userId, userSessionId=userSessionId, file=file)
