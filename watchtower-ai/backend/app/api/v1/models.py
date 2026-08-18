# pydantic schemas
from pydantic import BaseModel, Field
from typing import Optional, Dict

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    full_name: Optional[str]
    password: str

class UserRead(BaseModel):
    id: str
    email: str
    full_name: Optional[str]

class ModelUploadResponse(BaseModel):
    model_id: str
    name: str
    status: str
    message: Optional[str] = None
