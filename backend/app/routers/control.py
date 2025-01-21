from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from ..services.ros_bridge import RosBridgeService
import json
from typing import Dict
from datetime import datetime

router = APIRouter(tags=["control"])
ros_bridge = RosBridgeService()

# 속도 설정
LINEAR_SPEED = 0.26  # m/s
ANGULAR_SPEED = 1.82  # rad/s
DIAGONAL_LINEAR = 0.18  # 대각선 이동시 선속도 (30% 감소)
DIAGONAL_ANGULAR = 1.27  # 대각선 이동시 각속도 (30% 감소)

def create_twist_message(linear_x: float = 0.0, linear_y: float = 0.0, 
                        angular_z: float = 0.0) -> Dict:
    """ROS2 Twist 메시지 생성 (문자열 형태)"""
    return {
        "op": "publish",
        "topic": "/cmd_vel",
        "type": "geometry_msgs/msg/Twist",
        "msg": {
            "linear": {"x": str(linear_x), "y": str(linear_y), "z": "0.0"},
            "angular": {"x": "0.0", "y": "0.0", "z": str(angular_z)}
        }
    }

@router.websocket("/ws/control/{robot_id}")
async def control_robot(websocket: WebSocket, robot_id: str):
    """방향키 입력을 처리하는 WebSocket 엔드포인트"""
    await websocket.accept()
    
    # 현재 눌린 키를 추적
    pressed_keys = set()
    
    try:
        while True:
            # 프론트엔드로부터 키 입력 수신
            data = await websocket.receive_json()
            key = data.get("key")
            action = data.get("action", "keydown")  # keydown 또는 keyup
            
            # 키 상태 업데이트
            if action == "keydown":
                pressed_keys.add(key)
            elif action == "keyup":
                pressed_keys.discard(key)
            
            # 현재 눌린 키들에 기반하여 Twist 메시지 생성
            linear_x = 0.0
            angular_z = 0.0
            
            # 전진/후진 처리
            if "ArrowUp" in pressed_keys:
                linear_x = LINEAR_SPEED
            elif "ArrowDown" in pressed_keys:
                linear_x = -LINEAR_SPEED
            
            # 회전 처리
            if "ArrowLeft" in pressed_keys:
                angular_z = ANGULAR_SPEED
                # 전진/후진 중 회전시 속도 감소
                if linear_x != 0:
                    linear_x = linear_x * 0.7  # 30% 감소
                    angular_z = DIAGONAL_ANGULAR
            elif "ArrowRight" in pressed_keys:
                angular_z = -ANGULAR_SPEED
                # 전진/후진 중 회전시 속도 감소
                if linear_x != 0:
                    linear_x = linear_x * 0.7  # 30% 감소
                    angular_z = -DIAGONAL_ANGULAR
            
            # Twist 메시지 생성
            twist_msg = create_twist_message(
                linear_x=linear_x,
                angular_z=angular_z
            )
            
            print(f"[Backend] Sending to ROS: robot_id={robot_id}, linear_x={linear_x:.2f}, angular_z={angular_z:.2f}")
            
            # ROS2로 Twist 메시지 발행
            await ros_bridge.publish_to_topic(
                robot_id=robot_id,
                topic="/cmd_vel",
                msg_type="geometry_msgs/msg/Twist",
                data=twist_msg
            )
            
            print(f"[Backend] Message sent to ROS Bridge: {twist_msg}")
            
            # 프론트엔드에 피드백 전송
            await websocket.send_json({
                "status": "ok",
                "pressed_keys": list(pressed_keys),
                "twist": twist_msg,
                "timestamp": str(datetime.now())
            })
    
    except WebSocketDisconnect:
        # 연결이 끊어지면 로봇 정지
        await ros_bridge.publish_to_topic(
            robot_id=robot_id,
            topic="/cmd_vel",
            msg_type="geometry_msgs/Twist",
            data=create_twist_message()  # 모든 속도를 0으로 설정
        )
    except Exception as e:
        print(f"제어 에러 발생: {str(e)}")
        try:
            await websocket.send_json({
                "status": "error",
                "message": str(e)
            })
        except:
            pass 