
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path
from backend.api.v1.services.pdf_parser_service import parse_pdf
#from backend.api.v1.agents.chatbot_agents import ChatBotAgent


# Router initialization
router = APIRouter()


# Folder where PDFs will be stored
CURRENT_FILE = os.path.abspath(__file__)
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE))))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)



@router.post("/upload", summary="Upload PDF file")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a single PDF file and save it in the data directory.
    """
    try:
        # extracting file basic info details
        MAX_FILE_SIZE = 5 * 1024 * 1024
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(DATA_DIR, filename)
        file_bytes = await file.read()
        file_size = len(file_bytes)
        # print(f"file_size: {file_size}\n")
        # checking file extension
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        # checking file-size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large! Max 5 MB allowed.")
        # Write PDF file to disk
        with open(file_path, "wb") as f:
            # print(f"file_bytes: {file_bytes}\n")
            f.write(file_bytes)
        ### parsing the pdf file
        toParseFilePath = Path(DATA_DIR)/filename
        parsed_text = parse_pdf(toParseFilePath)
        print(f"parsed_text: {parsed_text}\n")
        if not parsed_text.strip():
            raise HTTPException(status_code=400, detail="PDF contains no readable text.")
        # returning response
        return JSONResponse(
            status_code=200,
            content={
                "message": f"File '{file.filename}' uploaded successfully.",
                "saved_as": filename,
                "path": file_path,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"upload_pdf error uploading file: {str(e)}")
