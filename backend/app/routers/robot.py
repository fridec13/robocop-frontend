from fastapi import APIRouter, HTTPException, Body
from ..services.ros_bridge import RosBridgeService
from ..models.robot import Robot, RobotStatus
from typing import List, Dict
import asyncio
from pydantic import BaseModel

router = APIRouter(prefix="/robot", tags=["robot"])
ros_bridge = RosBridgeService()

class RobotConnection(BaseModel):
    uri: str  # rosbridge_server WebSocket URI (예: ws://localhost:9090)
    robot_name: str = "Unknown Robot"

class RobotCommand(BaseModel):
    topic: str
    msg_type: str
    data: Dict

@router.post("/connect/{robot_id}")
async def connect_robot(robot_id: str, connection: RobotConnection):
    """rosbridge_server에 연결"""
    success = await ros_bridge.connect_to_robot(robot_id, connection.uri)
    if success:
        # 백그라운드에서 메시지 수신 시작
        asyncio.create_task(ros_bridge.start_listening(robot_id))
        return {
            "message": f"Robot {robot_id} 연결됨",
            "status": "connected",
            "robot_name": connection.robot_name
        }
    raise HTTPException(status_code=500, detail="로봇 연결 실패")

@router.post("/disconnect/{robot_id}")
async def disconnect_robot(robot_id: str):
    """로봇 연결 해제"""
    await ros_bridge.disconnect_from_robot(robot_id)
    return {"message": f"Robot {robot_id} 연결 해제됨", "status": "disconnected"}

@router.post("/publish/{robot_id}")
async def publish_to_topic(robot_id: str, command: RobotCommand):
    """ROS 토픽에 메시지 발행"""
    success = await ros_bridge.publish_to_topic(
        robot_id,
        command.topic,
        command.msg_type,
        command.data
    )
    if not success:
        raise HTTPException(status_code=500, detail="메시지 발행 실패")
    return {"message": "메시지가 발행됨", "command": command.dict()}

@router.get("/status/{robot_id}")
async def get_robot_status(robot_id: str):
    """로봇 상태 조회"""
    from ..database import robots
    status = await robots.find_one({"id": robot_id})
    if not status:
        raise HTTPException(status_code=404, detail="로봇을 찾을 수 없음")
    return status

@router.get("/list")
async def list_robots():
    """연결된 모든 로봇 목록 조회"""
    from ..database import robots
    robot_list = await robots.find(
        {"connection_status": "connected"},
        {"_id": 0}
    ).to_list(length=None)
    return robot_list 