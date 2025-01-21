import asyncio
import json
from typing import Dict, Optional, Callable
import aiohttp
from datetime import datetime
from ..database import robots, sensor_logs
from .websocket import WebSocketManager

class RosBridgeService:
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RosBridgeService, cls).__new__(cls)
            cls._instance.connections = {}  # robot_id: websocket connection
            cls._instance.ws_manager = WebSocketManager()
            cls._instance.message_handlers = {}
            cls._instance.session = None
            print("ROS Bridge 서비스 초기화됨")
        return cls._instance
    
    async def initialize(self):
        """aiohttp 세션 초기화"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    async def connect_to_robot(self, robot_id: str, uri: str):
        """rosbridge_server에 연결"""
        try:
            await self.initialize()
            
            if robot_id in self.connections:
                await self.disconnect_from_robot(robot_id)
            
            # rosbridge WebSocket 서버에 연결
            ws = await self.session.ws_connect(uri)
            self.connections[robot_id] = ws
            print(f"ROS Bridge 연결 성공 - Robot {robot_id}")
            
            # 연결 상태 업데이트
            await robots.update_one(
                {"id": robot_id},
                {"$set": {
                    "connection_status": "connected",
                    "last_connected": datetime.utcnow()
                }},
                upsert=True
            )
            
            # ROS 토픽 구독 시작
            await self._subscribe_to_topics(robot_id)
            return True
            
        except Exception as e:
            print(f"ROS Bridge 연결 실패 - Robot {robot_id}: {str(e)}")
            return False
    
    async def disconnect_from_robot(self, robot_id: str):
        """로봇과의 연결 해제"""
        if robot_id in self.connections:
            try:
                await self.connections[robot_id].close()
                print(f"ROS Bridge 연결 해제 - Robot {robot_id}")
            except Exception as e:
                print(f"ROS Bridge 연결 해제 중 에러 - Robot {robot_id}: {str(e)}")
            finally:
                self.connections.pop(robot_id, None)
                await robots.update_one(
                    {"id": robot_id},
                    {"$set": {
                        "connection_status": "disconnected",
                        "last_disconnected": datetime.utcnow()
                    }}
                )
    
    async def _subscribe_to_topics(self, robot_id: str):
        """ROS 토픽 구독"""
        topics = {
            "/robot_status": {
                "messageType": "std_msgs/String",
                "handler": self._handle_robot_status
            },
            "/sensor_data": {
                "messageType": "sensor_msgs/JointState",
                "handler": self._handle_sensor_data
            },
            "/camera_feed": {
                "messageType": "sensor_msgs/Image",
                "handler": self._handle_camera_feed
            },
            "/map_data": {
                "messageType": "nav_msgs/OccupancyGrid",
                "handler": self._handle_map_data
            }
        }
        
        for topic, config in topics.items():
            subscribe_msg = {
                "op": "subscribe",
                "topic": topic,
                "type": config["messageType"]
            }
            await self.send_message(robot_id, subscribe_msg)
            self.message_handlers[topic] = config["handler"]
    
    async def send_message(self, robot_id: str, message: dict):
        """ROS Bridge로 메시지 전송"""
        if robot_id not in self.connections:
            print(f"연결되지 않은 로봇 - Robot {robot_id}")
            return False
        
        try:
            await self.connections[robot_id].send_json(message)
            return True
        except Exception as e:
            print(f"메시지 전송 실패 - Robot {robot_id}: {str(e)}")
            return False
    
    async def publish_to_topic(self, robot_id: str, topic: str, msg_type: str, data: dict):
        """ROS 토픽에 메시지 발행"""
        message = {
            "op": "publish",
            "topic": topic,
            "type": msg_type,
            "msg": data
        }
        return await self.send_message(robot_id, message)
    
    async def start_listening(self, robot_id: str):
        """ROS Bridge로부터 메시지 수신 대기"""
        if robot_id not in self.connections:
            return
        
        ws = self.connections[robot_id]
        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data.get("op") == "publish":
                        await self._handle_message(robot_id, data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f"WebSocket 에러 발생 - Robot {robot_id}")
                    break
        except Exception as e:
            print(f"메시지 수신 중 에러 - Robot {robot_id}: {str(e)}")
        finally:
            await self.disconnect_from_robot(robot_id)
    
    async def _handle_message(self, robot_id: str, message: dict):
        """수신된 ROS 메시지 처리"""
        try:
            topic = message.get("topic")
            if topic in self.message_handlers:
                await self.message_handlers[topic](robot_id, message)
            
            # 프론트엔드로 메시지 전달
            message_type = topic.strip("/").replace("/", "_")
            await self.ws_manager.broadcast_to_robot(message, message_type, robot_id)
            
        except Exception as e:
            print(f"메시지 처리 중 에러: {str(e)}")
    
    async def _handle_robot_status(self, robot_id: str, message: dict):
        """로봇 상태 정보 처리"""
        status_data = message.get("msg", {})
        await robots.update_one(
            {"id": robot_id},
            {"$set": {
                "status": status_data,
                "last_updated": datetime.utcnow()
            }}
        )
    
    async def _handle_sensor_data(self, robot_id: str, message: dict):
        """센서 데이터 처리"""
        sensor_data = message.get("msg", {})
        await sensor_logs.insert_one({
            "robot_id": robot_id,
            "timestamp": datetime.utcnow(),
            "data": sensor_data
        })
    
    async def _handle_camera_feed(self, robot_id: str, message: dict):
        """카메라 피드 처리"""
        # 이미 camera_service에서 처리되고 있으므로 패스
        pass
    
    async def _handle_map_data(self, robot_id: str, message: dict):
        """지도 데이터 처리"""
        map_data = message.get("msg", {})
        await robots.update_one(
            {"id": robot_id},
            {"$set": {
                "map_data": map_data,
                "map_updated": datetime.utcnow()
            }}
        )
    
    async def cleanup(self):
        """서비스 정리"""
        if self.session:
            await self.session.close()
            self.session = None 