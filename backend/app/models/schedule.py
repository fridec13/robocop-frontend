from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import List, Optional
from enum import Enum

class WeekDay(str, Enum):
    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"
    SUN = "sun"

class ScheduleTime(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)

class Schedule(BaseModel):
    schedule_id: str = Field(...)  # 스케줄 고유 ID
    robot_id: str = Field(...)  # 로봇 ID
    time: ScheduleTime  # 실행 시간
    days: List[WeekDay]  # 실행 요일
    is_active: bool = Field(default=True)  # 활성화 여부
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "schedule_id": "schedule_001",
                "robot_id": "robot_001",
                "time": {
                    "hour": 14,
                    "minute": 30
                },
                "days": ["mon", "wed", "fri"],
                "is_active": True,
                "created_at": "2024-01-20T00:00:00",
                "updated_at": "2024-01-20T12:00:00"
            }
        } 