from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import json
import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
import numpy as np
import cv2
import base64
import time

# API 모델 정의
class User(BaseModel):
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False

class Robot(BaseModel):
    id: str
    name: str
    status: str
    battery_level: int

# 더미 데이터 저장소
class DataStore:
    def __init__(self):
        self.users = {
            "admin": {
                "username": "admin",
                "email": "admin@example.com",
                "password": "admin123",  # 실제로는 해시된 비밀번호를 사용해야 함
                "is_active": True,
                "is_admin": True
            }
        }
        self.robots = {
            f"ROBOT_{i:03d}": {
                "id": f"ROBOT_{i:03d}",
                "name": f"Robot {i}",
                "status": "idle",
                "battery_level": 100
            } for i in range(1, 6)
        }

db = DataStore()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin을 지정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# WebSocket CORS 미들웨어
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# WebSocket 연결 관리를 위한 클래스
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, List[WebSocket]]] = {
            "monitoring": {},  # robot_id별 연결 관리
            "camera": {},      # robot_id별 연결 관리
            "sensor": {},      # robot_id별 연결 관리
        }
        print("ConnectionManager 초기화됨")

    async def connect(self, websocket: WebSocket, client_type: str, robot_id: str):
        await websocket.accept()
        if robot_id not in self.active_connections[client_type]:
            self.active_connections[client_type][robot_id] = []
        self.active_connections[client_type][robot_id].append(websocket)
        print(f"새로운 WebSocket 연결: {client_type} - Robot {robot_id}")
        print(f"현재 연결 상태: {self.get_connection_status()}")

    def disconnect(self, websocket: WebSocket, client_type: str, robot_id: str):
        if robot_id in self.active_connections[client_type]:
            self.active_connections[client_type][robot_id].remove(websocket)
            if not self.active_connections[client_type][robot_id]:
                del self.active_connections[client_type][robot_id]
            print(f"WebSocket 연결 해제: {client_type} - Robot {robot_id}")
            print(f"현재 연결 상태: {self.get_connection_status()}")

    def get_connection_status(self):
        status = {}
        for client_type, robots in self.active_connections.items():
            status[client_type] = {
                robot_id: len(connections)
                for robot_id, connections in robots.items()
            }
        return status

    async def broadcast_to_robot(self, message: dict, client_type: str, robot_id: str):
        if robot_id in self.active_connections[client_type]:
            for connection in self.active_connections[client_type][robot_id]:
                await connection.send_json(message)

manager = ConnectionManager()

# 로그인 엔드포인트
@app.post("/token")
async def login(username: str, password: str):
    user = db.users.get(username)
    if not user or user["password"] != password:  # 실제로는 비밀번호 해시 비교를 해야 함
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return {"access_token": f"dummy_token_{username}", "token_type": "bearer"}

# 관리자용 사용자 생성 엔드포인트
@app.post("/admin/users")
async def create_user(username: str, email: str, password: str, is_admin: bool = False):
    if username in db.users:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db.users[username] = {
        "username": username,
        "email": email,
        "password": password,  # 실제로는 해시된 비밀번호를 저장해야 함
        "is_active": True,
        "is_admin": is_admin
    }
    return {"message": "User created successfully"}

# 관리자용 사용자 목록 조회
@app.get("/admin/users")
async def get_users():
    return list(db.users.values())

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

# 센서 데이터 생성 함수 (시뮬레이션)
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
        },
        "position": {
            "x": random.uniform(0, 100),
            "y": random.uniform(0, 100),
            "orientation": random.uniform(0, 360)
        }
    }

# WebSocket 엔드포인트 - 모니터링
@app.websocket("/ws/monitoring/{robot_id}")
async def websocket_monitoring(websocket: WebSocket, robot_id: str):
    try:
        await manager.connect(websocket, "monitoring", robot_id)
        print(f"모니터링 WebSocket 연결됨 - Robot {robot_id}")
        while True:
            data = generate_monitoring_data(robot_id)
            await websocket.send_json(data)
            print(f"모니터링 데이터 전송 - Robot {robot_id}: {data['status']}")
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "monitoring", robot_id)
        print(f"모니터링 WebSocket 연결 종료 - Robot {robot_id}")
    except Exception as e:
        print(f"모니터링 WebSocket 에러 - Robot {robot_id}: {str(e)}")
        manager.disconnect(websocket, "monitoring", robot_id)

# WebSocket 엔드포인트 - 센서 데이터
@app.websocket("/ws/sensor/{robot_id}")
async def websocket_sensor(websocket: WebSocket, robot_id: str):
    try:
        await manager.connect(websocket, "sensor", robot_id)
        print(f"센서 WebSocket 연결됨 - Robot {robot_id}")
        while True:
            data = generate_sensor_data(robot_id)
            await websocket.send_json(data)
            print(f"센서 데이터 전송 - Robot {robot_id}")
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "sensor", robot_id)
        print(f"센서 WebSocket 연결 종료 - Robot {robot_id}")
    except Exception as e:
        print(f"센서 WebSocket 에러 - Robot {robot_id}: {str(e)}")
        manager.disconnect(websocket, "sensor", robot_id)

# 카메라 캡처 클래스 수정
class CameraManager:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CameraManager, cls).__new__(cls)
            cls._instance.cameras = {}
            cls._instance.active_streams = {}
            print("카메라 매니저 초기화됨")
        return cls._instance

    async def get_camera(self, robot_id: str):
        async with self._lock:
            if robot_id not in self.cameras:
                try:
                    # 카메라 초기화 시도
                    for camera_index in range(2):  # 카메라 인덱스 0과 1 시도
                        try:
                            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # DirectShow 백엔드 사용
                            if cap.isOpened():
                                # 카메라 설정
                                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                                cap.set(cv2.CAP_PROP_FPS, 30)
                                
                                # 테스트 프레임 읽기
                                ret, frame = cap.read()
                                if ret:
                                    self.cameras[robot_id] = cap
                                    self.active_streams[robot_id] = True
                                    print(f"카메라 열림 - Robot {robot_id} (인덱스: {camera_index})")
                                    print(f"카메라 설정: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)} @ {cap.get(cv2.CAP_PROP_FPS)}fps")
                                    return self.cameras[robot_id]
                                else:
                                    cap.release()
                                    print(f"카메라 {camera_index}에서 프레임을 읽을 수 없음")
                            else:
                                print(f"카메라 {camera_index}를 열 수 없음")
                        except Exception as e:
                            print(f"카메라 {camera_index} 초기화 중 에러: {str(e)}")
                            if cap:
                                cap.release()
                    
                    # 모든 카메라 시도 실패
                    raise Exception("사용 가능한 카메라를 찾을 수 없습니다")
                    
                except Exception as e:
                    print(f"카메라 초기화 에러 - Robot {robot_id}: {str(e)}")
                    raise
            return self.cameras[robot_id]

    def release_camera(self, robot_id: str):
        if robot_id in self.cameras:
            try:
                self.active_streams[robot_id] = False
                self.cameras[robot_id].release()
                print(f"카메라 해제됨 - Robot {robot_id}")
            except Exception as e:
                print(f"카메라 해제 중 에러 - Robot {robot_id}: {str(e)}")
            finally:
                if robot_id in self.cameras:
                    del self.cameras[robot_id]
                if robot_id in self.active_streams:
                    del self.active_streams[robot_id]

    def is_active(self, robot_id: str):
        return self.active_streams.get(robot_id, False)

camera_manager = CameraManager()

# WebSocket 엔드포인트 - 카메라 스트림
@app.websocket("/ws/camera/{robot_id}")
async def websocket_camera(websocket: WebSocket, robot_id: str):
    try:
        await manager.connect(websocket, "camera", robot_id)
        print(f"카메라 WebSocket 연결됨 - Robot {robot_id}")
        
        cap = await camera_manager.get_camera(robot_id)
        frame_number = 0
        error_count = 0
        max_errors = 3
        
        while camera_manager.is_active(robot_id):
            try:
                ret, frame = cap.read()
                if not ret:
                    error_count += 1
                    print(f"프레임 읽기 실패 ({error_count}/{max_errors}) - Robot {robot_id}")
                    if error_count >= max_errors:
                        await websocket.send_json({"error": "카메라에서 프레임을 읽을 수 없습니다"})
                        break
                    await asyncio.sleep(1)
                    continue

                error_count = 0  # 성공하면 에러 카운트 리셋
                
                # 프레임 크기 조정 (네트워크 부하 감소)
                frame = cv2.resize(frame, (640, 480))
                
                # JPEG으로 인코딩
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                
                # Base64로 인코딩
                base64_image = base64.b64encode(buffer).decode('utf-8')
                
                camera_data = {
                    "robot_id": robot_id,
                    "frame_number": frame_number,
                    "timestamp": datetime.now().isoformat(),
                    "image": base64_image,
                    "status": "streaming"
                }
                
                await websocket.send_json(camera_data)
                frame_number += 1
                
                # 프레임 레이트 조절
                await asyncio.sleep(0.033)  # 약 30fps
                
            except Exception as e:
                print(f"프레임 처리 중 에러 - Robot {robot_id}: {str(e)}")
                error_count += 1
                if error_count >= max_errors:
                    await websocket.send_json({"error": str(e)})
                    break
                await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        print(f"카메라 WebSocket 연결 종료 - Robot {robot_id}")
        camera_manager.release_camera(robot_id)
        manager.disconnect(websocket, "camera", robot_id)
    except Exception as e:
        print(f"카메라 WebSocket 에러 - Robot {robot_id}: {str(e)}")
        camera_manager.release_camera(robot_id)
        manager.disconnect(websocket, "camera", robot_id)
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass

# 카메라 상태 확인 API
@app.get("/api/camera/status")
async def get_camera_status():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {"status": "error", "message": "카메라를 열 수 없습니다"}
        
        ret, _ = cap.read()
        cap.release()
        
        if not ret:
            return {"status": "error", "message": "카메라에서 프레임을 읽을 수 없습니다"}
            
        return {"status": "ok", "message": "카메라가 정상적으로 작동 중입니다"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# REST API 엔드포인트 - 로봇 목록
@app.get("/api/robots")
async def get_robots():
    return [generate_monitoring_data(robot_id) for robot_id in db.robots.keys()]

# 관리자용 로봇 관리 엔드포인트
@app.post("/admin/robots")
async def create_robot(robot_id: str, name: str):
    if robot_id in db.robots:
        raise HTTPException(status_code=400, detail="Robot ID already exists")
    
    db.robots[robot_id] = {
        "id": robot_id,
        "name": name,
        "status": "idle",
        "battery_level": 100
    }
    return db.robots[robot_id]

async def generate_point_cloud_data() -> Dict[str, Any]:
    # 100개의 3D 포인트 생성
    num_points = 100
    x = np.random.uniform(-5, 5, num_points)
    y = np.random.uniform(-5, 5, num_points)
    z = np.random.uniform(0, 3, num_points)
    
    # intensity 값 생성 (0-1 사이)
    intensity = np.random.uniform(0, 1, num_points)
    
    # numpy 배열을 리스트로 변환
    points = [
        {
            "x": float(x[i]),
            "y": float(y[i]),
            "z": float(z[i]),
            "intensity": float(intensity[i])
        }
        for i in range(num_points)
    ]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "points": points
    }

@app.websocket("/ws/lidar")
async def websocket_lidar_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("LiDAR WebSocket 연결됨")
    try:
        while True:
            point_cloud = await generate_point_cloud_data()
            await websocket.send_json(point_cloud)
            print(f"LiDAR 데이터 전송: {len(point_cloud['points'])} 포인트")
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("LiDAR WebSocket 연결 종료")
    except Exception as e:
        print(f"LiDAR WebSocket 에러: {str(e)}")

async def generate_camera_frame():
    """실제 카메라에서 프레임을 캡처하는 함수"""
    print("웹캠 연결 시도 중...")
    cap = cv2.VideoCapture(0)  # 기본 웹캠 사용
    
    if not cap.isOpened():
        print("카메라를 열 수 없습니다! 다음을 확인해주세요:")
        print("1. 웹캠이 연결되어 있는지")
        print("2. 다른 프로그램이 웹캠을 사용 중인지")
        print("3. 웹캠 드라이버가 정상적으로 설치되어 있는지")
        return
    
    print(f"웹캠 연결 성공!")
    print(f"해상도: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
    print(f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없습니다!")
                print("카메라 상태:", "연결됨" if cap.isOpened() else "연결 끊김")
                break
                
            # 프레임 크기 조정
            frame = cv2.resize(frame, (640, 480))
            
            # JPEG으로 인코딩
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            # Base64로 인코딩
            image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            yield {
                'image': image_base64,
                'timestamp': datetime.now().isoformat(),
                'camera_status': 'active'
            }
            
            await asyncio.sleep(0.033)  # 약 30 FPS
    
    except Exception as e:
        print(f"카메라 캡처 중 에러 발생: {str(e)}")
        yield {
            'error': str(e),
            'camera_status': 'error'
        }
    
    finally:
        print("카메라 연결 종료")
        cap.release()

@app.websocket("/ws/camera/{camera_id}")
async def camera_stream(websocket: WebSocket, camera_id: str):
    try:
        await manager.connect(websocket, "camera", camera_id)
        print(f"카메라 스트림 시작 - Camera ID: {camera_id}")
        
        async for frame in generate_camera_frame():
            if websocket.client_state.CONNECTED:
                await websocket.send_json(frame)
            else:
                break
                
    except WebSocketDisconnect:
        print(f"클라이언트 연결 종료 - Camera ID: {camera_id}")
        manager.disconnect(websocket, "camera", camera_id)
        
    except Exception as e:
        print(f"카메라 스트리밍 에러 - Camera ID: {camera_id}, 에러: {str(e)}")
        manager.disconnect(websocket, "camera", camera_id)
        try:
            await websocket.send_json({
                'error': str(e),
                'camera_status': 'error'
            })
        except:
            pass

# 서버 시작
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 