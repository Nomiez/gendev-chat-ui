from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    salt: str
    company_name: str
    info_text: str
    profile_picture: str
    keywords: list[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPost(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    info_text: str
    company_name: str
    keywords: list[str]


class UserPostExtended(UserPost):
    salt: str
    profile_picture: str


class UserGet(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    info_text: str
    company_name: str
    keywords: list[str]
    profile_picture: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPut(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    info_text: Optional[str] = None
    company_name: Optional[str] = None
    keywords: Optional[list[str]] = None


class UserAttach(UserPut):
    user_id: int


class UserPutExtended(UserPut):
    password: Optional[str] = None
    salt: Optional[str] = None
    profile_picture: Optional[str] = None

    class Config:
        from_attributes = True


class UserGetFiltered(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    profile_picture: str
    info_text: str
    keywords: list[str]

    class Config:
        from_attributes = True


class UserInReview(BaseModel):
    first_name: str
    last_name: str
    profile_picture: str

    class Config:
        from_attributes = True
