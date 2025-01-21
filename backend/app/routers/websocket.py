from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.websocket import WebSocketManager
from ..services.camera import CameraService
import asyncio
import random
from datetime import datetime

router = APIRouter()
ws_manager = WebSocketManager()
camera_service = CameraService()

# 모니터링 데이터 생성 함수
def generate_monitoring_data(robot_id: str):
    return {
        "id": robot_id,
        "status": random.choice(["active", "charging", "idle", "error"]),
        "battery": random.randint(20, 100),
        "location": {
            "x": random.uniform(0, 100),
            "y": random.uniform(0, 100)
        },
        "current_task": random.choice([None, "patrol", "delivery", "cleaning"]),
        "last_updated": datetime.now().isoformat()
    }

# 센서 데이터 생성 함수
def generate_sensor_data(robot_id: str):
    return {
        "robot_id": robot_id,
        "timestamp": datetime.now().isoformat(),
        "lidar_data": {
            "points": [
                {"x": random.uniform(-10, 10), "y": random.uniform(-10, 10)}
                for _ in range(360)
            ]
        },
        "imu_data": {
            "acceleration": {
                "x": random.uniform(-1, 1),
                "y": random.uniform(-1, 1),
                "z": random.uniform(-1, 1)
            },
            "gyro": {
                "x": random.uniform(-1, 1),
                "y": random.uniform(-1, 1),
                "z": random.uniform(-1, 1)
            }
        }
    }

@router.websocket("/ws/monitoring/{robot_id}")
async def websocket_monitoring(websocket: WebSocket, robot_id: str):
    try:
        await ws_manager.connect(websocket, "monitoring", robot_id)
        while True:
            data = generate_monitoring_data(robot_id)
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "monitoring", robot_id)
    except Exception as e:
        print(f"모니터링 WebSocket 에러 - Robot {robot_id}: {str(e)}")
        ws_manager.disconnect(websocket, "monitoring", robot_id)

@router.websocket("/ws/sensor/{robot_id}")
async def websocket_sensor(websocket: WebSocket, robot_id: str):
    try:
        await ws_manager.connect(websocket, "sensor", robot_id)
        while True:
            data = generate_sensor_data(robot_id)
            await websocket.send_json(data)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "sensor", robot_id)
    except Exception as e:
        print(f"센서 WebSocket 에러 - Robot {robot_id}: {str(e)}")
        ws_manager.disconnect(websocket, "sensor", robot_id)

@router.websocket("/ws/camera/{robot_id}")
async def websocket_camera(websocket: WebSocket, robot_id: str):
    try:
        await ws_manager.connect(websocket, "camera", robot_id)
        await camera_service.get_camera(robot_id)
        
        frame_number = 0
        while camera_service.is_active(robot_id):
            frame_data = await camera_service.get_frame(robot_id)
            if frame_data:
                frame_data["frame_number"] = frame_number
                frame_data["robot_id"] = robot_id
                await websocket.send_json(frame_data)
                await camera_service.log_frame(robot_id, frame_number, None, "streaming")
                frame_number += 1
            await asyncio.sleep(0.033)
            
    except WebSocketDisconnect:
        camera_service.release_camera(robot_id)
        ws_manager.disconnect(websocket, "camera", robot_id)
    except Exception as e:
        print(f"카메라 WebSocket 에러 - Robot {robot_id}: {str(e)}")
        camera_service.release_camera(robot_id)
        ws_manager.disconnect(websocket, "camera", robot_id)
        try:
            await websocket.send_json({"error": str(e)})
        except Exception:
            pass 