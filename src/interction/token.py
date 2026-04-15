import uuid
from typing import Tuple
from fastapi import HTTPException
import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def decode_user_token(authorization_header: str) -> Tuple[uuid.UUID, str]:
    try:
        token_parts = authorization_header.split(" ")

        if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authorization header format! Must be 'Bearer <token>'",
            )

        raw_token = token_parts[1]

        payload = jwt.decode(raw_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uid_str: str = payload.get("sub")
        user_uid = uuid.UUID(user_uid_str)
        username: str = payload.get("username")

        if not user_uid:
            raise HTTPException(status_code=401, detail="User UID not found in token payload!")
        
        if not username:
            raise HTTPException(status_code=401, detail="Username not found in token payload!")

        return user_uid, username

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token time out")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Token is invalid or has been tampered with!"
        )
