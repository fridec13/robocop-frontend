from fastapi import WebSocket
from typing import Dict, List
from datetime import datetime
from ..database import websocket_logs

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, List[WebSocket]]] = {
            "monitoring": {},  # robot_id별 연결 관리
            "camera": {},      # robot_id별 연결 관리
            "sensor": {},      # robot_id별 연결 관리
        }
        print("WebSocket 매니저 초기화됨")
    
    async def connect(self, websocket: WebSocket, client_type: str, robot_id: str):
        await websocket.accept()
        if robot_id not in self.active_connections[client_type]:
            self.active_connections[client_type][robot_id] = []
        self.active_connections[client_type][robot_id].append(websocket)
        await self.log_event(client_type, robot_id, "connected", {})
        print(f"새로운 WebSocket 연결: {client_type} - Robot {robot_id}")
    
    def disconnect(self, websocket: WebSocket, client_type: str, robot_id: str):
        if robot_id in self.active_connections[client_type]:
            self.active_connections[client_type][robot_id].remove(websocket)
            if not self.active_connections[client_type][robot_id]:
                del self.active_connections[client_type][robot_id]
            print(f"WebSocket 연결 해제: {client_type} - Robot {robot_id}")
    
    async def broadcast_to_robot(self, message: dict, client_type: str, robot_id: str):
        if robot_id in self.active_connections[client_type]:
            for connection in self.active_connections[client_type][robot_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"메시지 전송 실패: {str(e)}")
                    await self.disconnect(connection, client_type, robot_id)
    
    def get_connection_status(self) -> Dict:
        return {
            client_type: {
                robot_id: len(connections)
                for robot_id, connections in robots.items()
            }
            for client_type, robots in self.active_connections.items()
        }
    
    async def log_event(self, connection_type: str, robot_id: str, event_type: str, data: dict):
        await websocket_logs.insert_one({
            "connection_type": connection_type,
            "robot_id": robot_id,
            "timestamp": datetime.utcnow(),
            "event_type": event_type,
            "data": data
        }) 