
from typing import List

def standard_response(status_code:int=200, messages:list=None, data=None):
    return {
        "status_code": status_code,
        "messages": messages,
        "data": data
    }