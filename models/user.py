from pydantic import BaseModel, EmailStr


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    role: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str
