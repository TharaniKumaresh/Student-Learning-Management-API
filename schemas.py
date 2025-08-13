from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(min_length=6)
    role: str = "student"

class UserOut(UserBase):
    id: int
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CourseBase(BaseModel):
    title: str
    description: str = ""
    published: bool = True

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    published: Optional[bool] = None

class CourseOut(CourseBase):
    id: int
    class Config:
        from_attributes = True

class EnrollmentOut(BaseModel):
    id: int
    course: CourseOut
    class Config:
        from_attributes = True
