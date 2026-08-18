from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    class Config:
        orm_mode = True