

# loading all required modules
import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
load_dotenv()
from backend.api.v1.core import MysqlDB
from backend.api.v1.routes import chat_routes, pdf_routes

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
app.include_router(chat_routes.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(pdf_routes.router, prefix="/api/v1/pdf", tags=["PDF"])

# app startup events
# database open connections
@app.on_event("startup")
async def startup_event():
    print(f"Application startup: connecting to MySQL database...\n")
    RETRY_INTERVAL = 3
    MAX_RETRIES = 20
    retries = 0
    while retries < MAX_RETRIES:
        try:
            await MysqlDB.connect()
            print("Application startup: connected to MySQL database...\n")
            break
        except Exception as e:
            retries+= 1
            print(f"Waiting for MySQL... attempt {retries}/{MAX_RETRIES}, error: {e}\n")
            await asyncio.sleep(RETRY_INTERVAL)
    else:
        raise RuntimeError("Could not connect to MySQL after multiple attempts")
    
# app shutdown events
# database close connections
@app.on_event("shutdown")
async def shutdown_event():
    print(f"Application shutdown: disconnecting from MySQL database...\n")
    await MysqlDB.disconnect()
    print(f"Application shutdown: disconnected from MySQL database...\n")



# system-health endpoint
@app.get("/system-health", summary="System Health")
async def root():
    """
        This api is used for checking backend system health
    """
    return {"message": "DocumentQAChatBot Backend is Running"}


# main server runner
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True  # Turn off in production
    )
