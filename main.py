

# loading all required modules
from dotenv import load_dotenv
import os
load_dotenv()
import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.api.v1.routes import system_routes
from backend.api.v1.routes import login_routes
from backend.api.v1.routes import chat_routes
from backend.api.v1.routes import pdf_routes
from backend.api.v1.utils.utils import *


# initialize the app
app = FastAPI(
    title="DocumentQAChatBot APIs",
    description="Backend APIs for document-based QA chatbot system",    
    version="1.0.0",
)

# Configure CORS (for frontend UI)
origins = [
    os.getenv("FRONTEND_URL", "http://127.0.0.1:8080"),
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API Routes
app.include_router(login_routes.router, prefix="/api/v1/login", tags=["Login"])
app.include_router(system_routes.router, prefix="/api/v1/system", tags=["System"])
app.include_router(chat_routes.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(pdf_routes.router, prefix="/api/v1/pdf", tags=["PDF"])


# app startup events
@app.on_event("startup")
async def startup_event():
    print(f"Application startup...\n")
    
    
# app shutdown events
@app.on_event("shutdown")
async def shutdown_event():
    print(f"Application shutdown...\n")


# main server runner
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True
    )
