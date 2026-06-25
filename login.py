from fastapi import APIRouter, Form, HTTPException
from auth import create_access_token

router = APIRouter()


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):

    if username != "admin" or password != "admin123":
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {"sub": username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }