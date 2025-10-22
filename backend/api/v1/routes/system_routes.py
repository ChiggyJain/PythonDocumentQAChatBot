
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.api.v1.utils.utils import *

router = APIRouter()


# system-health endpoint
@router.get("/system-health", summary="Check Backend System Health")
async def check_system_health():
    """
        This api is used for checking backend system health
    """
    return JSONResponse(
        status_code=200,
        content=standard_response(
            status_code=200,
            messages=[f"DocumentQAChatBot Backend System is Up & Running"],
            data={}
        ) 
    )