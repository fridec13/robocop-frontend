import cv2
import base64
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from ..database import camera_logs

class CameraService:
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CameraService, cls).__new__(cls)
            cls._instance.cameras = {}
            cls._instance.active_streams = {}
            print("카메라 서비스 초기화됨")
        return cls._instance
    
    async def get_camera(self, robot_id: str):
        async with self._lock:
            if robot_id not in self.cameras:
                try:
                    for camera_index in range(2):
                        try:
                            cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
                            if cap.isOpened():
                                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                                cap.set(cv2.CAP_PROP_FPS, 30)
                                
                                ret, frame = cap.read()
                                if ret:
                                    self.cameras[robot_id] = cap
                                    self.active_streams[robot_id] = True
                                    print(f"카메라 열림 - Robot {robot_id} (인덱스: {camera_index})")
                                    return self.cameras[robot_id]
                                else:
                                    cap.release()
                        except Exception as e:
                            print(f"카메라 {camera_index} 초기화 중 에러: {str(e)}")
                            if 'cap' in locals():
                                cap.release()
                    
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
                self.cameras.pop(robot_id, None)
                self.active_streams.pop(robot_id, None)
    
    def is_active(self, robot_id: str) -> bool:
        return self.active_streams.get(robot_id, False)
    
    async def get_frame(self, robot_id: str) -> Optional[Dict[str, Any]]:
        if not self.is_active(robot_id):
            return None
            
        cap = self.cameras.get(robot_id)
        if not cap:
            return None
            
        ret, frame = cap.read()
        if not ret:
            return None
            
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        base64_image = base64.b64encode(buffer).decode('utf-8')
        
        return {
            "image": base64_image,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
    
    async def log_frame(self, robot_id: str, frame_number: int, image_path: Optional[str], status: str):
        await camera_logs.insert_one({
            "robot_id": robot_id,
            "timestamp": datetime.utcnow(),
            "frame_number": frame_number,
            "image_path": image_path,
            "status": status
        }) 