from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class RobotStatus(str, Enum):
    IDLE = "idle"
    MOVING = "moving"
    CHARGING = "charging"
    ERROR = "error"
    OFFLINE = "offline"

class Position(BaseModel):
    x: float = Field(...)
    y: float = Field(...)
    theta: float = Field(...)

class BatteryStatus(BaseModel):
    level: float = Field(..., ge=0, le=100)  # 배터리 잔량 (%)
    is_charging: bool = Field(default=False)  # 충전 중 여부

class Robot(BaseModel):
    robot_id: int = Field(...)  # 로봇 고유 ID (자동 증가하는 정수)
    name: str = Field(...)  # 로봇 이름
    ip_address: str = Field(...)  # 로봇 IP 주소
    status: RobotStatus = Field(default=RobotStatus.IDLE)  # 로봇 상태
    position: Position  # 현재 위치
    battery: BatteryStatus  # 배터리 상태
    last_active: datetime = Field(default_factory=datetime.now)  # 마지막 활성 시간
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "robot_id": 1,
                "name": "Security Bot 1",
                "ip_address": "192.168.1.100",
                "status": "idle",
                "position": {
                    "x": 10.5,
                    "y": 20.3,
                    "theta": 1.57
                },
                "battery": {
                    "level": 85.5,
                    "is_charging": False
                },
                "last_active": "2024-01-20T15:30:00",
                "created_at": "2024-01-20T00:00:00",
                "updated_at": "2024-01-20T15:30:00"
            }
        } 