from fastapi import APIRouter, BackgroundTasks, Depends, Response, status, Request
from fastapi.responses import JSONResponse
from src.database import database

router = APIRouter()

import hashlib


def hash_password(password):
    # Create a new SHA3_256 hash object
    hash_object = hashlib.sha3_256()

    # Hash the password by encoding it as UTF-8 and updating the hash object
    hash_object.update(password.encode("utf-8"))

    # Get the hexadecimal representation of the hash
    hashed_password = hash_object.hexdigest()

    return hashed_password


def check_database(data):
    result = database.get_collection("account").find_one({"id": data["id"]})
    if result:
        return True
    else:
        return False


@router.post("/newaccount")
async def test(request: Request):
    data = await request.json()
    ## data format: {"id": "abc", "password": "123"}
    if check_database(data):
        result = {"message": "Account already exists"}
        return JSONResponse(content=result, status_code=status.HTTP_404_NOT_FOUND)
    else:
        password = data["password"]
        hashed_password = hash_password(password)
        data_input_db = {"id": data["id"], "password": hashed_password}
        database.get_collection("account").insert_one(data_input_db)

        return JSONResponse(content={"message": "Done"}, status_code=status.HTTP_200_OK)


@router.get("/get")
def get():
    data = {"message": "Hello World"}
    return JSONResponse(content=data, status_code=status.HTTP_404_NOT_FOUND)
