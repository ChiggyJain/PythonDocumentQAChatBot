
from typing import List, Any

def standard_response(status_code:int=200, messages:list=None, data=Any):
    return {
        "status_code": status_code,
        "messages": messages,
        "data": data
    }