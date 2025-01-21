from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

class User(BaseModel):
    user_id: str = Field(...)  # 사용자 고유 ID
    email: EmailStr = Field(...)  # 이메일
    password: str = Field(...)  # 비밀번호 (해시된 값)
    name: str = Field(...)  # 이름
    role: UserRole = Field(default=UserRole.VIEWER)  # 사용자 역할
    is_active: bool = Field(default=True)  # 계정 활성화 여부
    last_login: Optional[datetime] = None  # 마지막 로그인 시간
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_001",
                "email": "admin@example.com",
                "password": "hashed_password_value",
                "name": "Admin User",
                "role": "admin",
                "is_active": True,
                "last_login": "2024-01-20T15:30:00",
                "created_at": "2024-01-20T00:00:00",
                "updated_at": "2024-01-20T15:30:00"
            }
        }

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)  # 최소 8자리 이상
    name: str
    role: Optional[UserRole] = UserRole.VIEWER

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    name: str
    role: UserRole
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime] 