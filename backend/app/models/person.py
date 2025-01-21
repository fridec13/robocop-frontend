from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class PersonType(str, Enum):
    EMPLOYEE = "employee"
    VISITOR = "visitor"
    UNKNOWN = "unknown"

class ImageInfo(BaseModel):
    image_id: str = Field(...)  # 이미지 고유 ID
    url: str = Field(...)  # 이미지 URL
    created_at: datetime = Field(default_factory=datetime.now)

class Person(BaseModel):
    person_id: str = Field(...)  # 사람 고유 ID
    name: str = Field(...)  # 이름
    type: PersonType = Field(default=PersonType.UNKNOWN)  # 사람 유형
    images: List[ImageInfo]  # 등록된 이미지 목록
    description: Optional[str] = None  # 설명
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "person_id": "person_001",
                "name": "John Doe",
                "type": "employee",
                "images": [
                    {
                        "image_id": "img_001",
                        "url": "https://example.com/images/person_001_1.jpg",
                        "created_at": "2024-01-20T00:00:00"
                    },
                    {
                        "image_id": "img_002",
                        "url": "https://example.com/images/person_001_2.jpg",
                        "created_at": "2024-01-20T00:00:00"
                    }
                ],
                "description": "Software Engineer",
                "created_at": "2024-01-20T00:00:00",
                "updated_at": "2024-01-20T12:00:00"
            }
        } 