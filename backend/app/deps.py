from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from app.config import API_TOKEN

async def token_guard(x_api_token: Optional[str] = Header(None)):
    if x_api_token is None or x_api_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Token",
        )
