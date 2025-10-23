
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path
from backend.api.v1.services.pdf_parser_service import parse_pdf
from backend.api.v1.schemas.pdf_schema import *
from backend.api.v1.agents.chatbot_agents import ChatBotAgent
from backend.api.v1.utils.utils import *

router = APIRouter()
chatBotAgentManager = ChatBotAgent()
# print(f"pdf-routes-chatBotAgentManager-id: {id(chatBotAgentManager)}\n")


# Folder where PDFs will be stored
CURRENT_FILE = os.path.abspath(__file__)
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE))))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)



@router.post("/upload", summary="Upload Single PDF file")
async def upload_pdf(uploading_file_request:UploadPdfFileRequest=Depends(UploadPdfFileRequest.as_form)):
    """
    Upload a single PDF file and save it in the data directory.
    """
    try:
        # extracting request param details
        file = uploading_file_request.file
        userId = uploading_file_request.userId
        userSessionId = uploading_file_request.userSessionId
        MAX_FILE_SIZE = 5 * 1024 * 1024
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(DATA_DIR, filename)
        file_bytes = await file.read()
        file_size = len(file_bytes)
        # print(f"file_size: {file_size}\n")
        # checking file extension
        if not filename.lower().endswith(".pdf"):
            return JSONResponse(
                status_code=400,
                content=standard_response(
                    status_code=400, messages=[f"Only PDF files are allowed"], data={}
                )
            )
        # checking empty
        if file_size<=0:
            return JSONResponse(
                status_code=400,
                content=standard_response(
                    status_code=400, messages=[f"uploaded pdf file is empty."], data={}
                )
            )
        # checking file-size
        if file_size > MAX_FILE_SIZE:
            return JSONResponse(
                status_code=400,
                content=standard_response(
                    status_code=400, messages=[f"File too large! Max 5 MB allowed."], data={}
                )
            )
        # Write PDF file to disk
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        ### parsing the pdf file
        toParseFilePath = Path(DATA_DIR)/filename
        parsed_file_result_dict = parse_pdf(toParseFilePath)
        # print(f"parsed_file_result_dict: {parsed_file_result_dict}\n")
        if len(parsed_file_result_dict['allPagesDetails'])<=0:
            return JSONResponse(
                status_code=400,
                content=standard_response(
                    status_code=400, messages=[f"Uploaded pdf file contains no readable text."], data={}
                )
            )
        # adding knowledge to agent
        agentInstancesDict = chatBotAgentManager.get_or_create_agent(userId, userSessionId)
        agentInstancesDict['all_pdf_text'].append(parsed_file_result_dict['overallPdfSummary'])
        agentInstancesDict['overall_pdf_text']+= "\n" + parsed_file_result_dict['overallPdfSummary']['content']
        # print(f"agentInstancesDict: {agentInstancesDict}")
        # returning response
        return JSONResponse(
            status_code=200,
            content=standard_response(
                status_code=200, messages=[f"File '{file.filename}' is uploaded successfully and ready for QA."], data={
                    "filePath" : file_path, "fileName" : filename
                }
            )
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=standard_response(
                status_code=500, messages=[f"Error occured while uploading pdf file: {str(e)}"], data={}
            )
        )