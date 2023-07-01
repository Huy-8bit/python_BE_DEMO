from fastapi import APIRouter, BackgroundTasks, Depends, Response, status, Request
from fastapi.responses import JSONResponse
from src.database import database
from src.auth.jwt import *

router = APIRouter()

import hashlib


def check_id_Account(data):
    result = database.get_collection("account").find_one({"id": data["id"]})
    if result:
        return True
    else:
        return False


@router.get("/get")
async def get(request: Request):
    data = {"message": "Hello World"}
    data_header = request.headers["signature"]
    check_access_token = await parse_jwt_user_data_optional(data_header)
    print("check:", check_access_token)
    if check_access_token:
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)

    else:
        return JSONResponse(
            content={"message": "Access Token is invalid"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
