import os
import jwt
from fastapi import Header, HTTPException, status
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET = os.getenv("INTERNAL_AUTH_SECRET")

def verify_internal_token(
    authorization: str = Header(..., description="Bearer token")
):
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return payload
