

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.api.v1.schemas.login_schema import *
from backend.api.v1.utils.utils import *

router = APIRouter()


# login api
@router.post("/authenticate_login_user/", summary="User Login Authentication")
async def authenticate_login_user(loginUserRequestFormData: LoginRequest):
    """
        This api is used for authenticate user login details. 
        If login success then return access-token details with validity of 15minutes only for accessing other apis [Right now this part is not implemented].
        If login success then use return userId, userSessionId for other apis accessing.
        If login failed then return error messages.
        - **username**: Enter your account username
        - **password**: Enter your account password
        - Demo Credentials: 
            1) Username: admin1, Password: admin1
            2) Username: admin2, Password: admin2
    """
    loginRspObj = standard_response(status_code=401, messages=["Invalid username or password."], data={})
    try:
        # print(f"loginUserRequestFormData: {loginUserRequestFormData}\n")
        dummyUserLoginDict = {
            "admin1" : {
                "password" : "admin1", "userId" : "11"
            },
            "admin2" : {
                "password" : "admin2", "userId" : "12"
            },
            "admin3" : {
                "password" : "admin3", "userId" : "13"
            }
        }
        if loginUserRequestFormData.username in dummyUserLoginDict:
            loginRspObj['status_code'] = 200
            loginRspObj['messages'] = [f"User login successfully and User-ID: {dummyUserLoginDict[loginUserRequestFormData.username]['userId']}"]
            loginRspObj['data'] = {
                "userId" : dummyUserLoginDict[loginUserRequestFormData.username]['userId']
            }
        else:
            loginRspObj['status_code'] = 401
            loginRspObj['messages'] = ["Invalid username or password."]
    except Exception as e:
        loginRspObj['status_code'] = 500
        loginRspObj['messages'] = [f"Error occured: {str(e)}"]
    return JSONResponse(status_code=loginRspObj['status_code'], content=loginRspObj)