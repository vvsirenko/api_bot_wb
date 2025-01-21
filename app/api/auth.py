from fastapi import Header, HTTPException, Depends
from typing import Optional
from app import config


async def get_token(x_token: Optional[str] = Header(None)) -> str:
    if x_token != config.API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Token")
    return x_token