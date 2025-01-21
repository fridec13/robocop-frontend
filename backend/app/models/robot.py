from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class Location(BaseModel):
    x: float
    y: float

class RobotStatus(BaseModel):
    id: str
    status: str
    battery: int
    location: Location
    current_task: Optional[str]
    last_updated: datetime

class SensorData(BaseModel):
    robot_id: str
    timestamp: datetime
    lidar_data: Dict[str, List[Dict[str, float]]]
    imu_data: Dict[str, Dict[str, float]]
    position: Dict[str, float]

class CameraFrame(BaseModel):
    robot_id: str
    frame_number: int
    timestamp: datetime
    image: str  # base64 encoded image
    status: str

class Robot(BaseModel):
    id: str
    name: str
    status: str = "idle"
    battery_level: int = 100 