from fastapi import APIRouter, Path, Query, HTTPException
from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime
from ..schemas.responses import BaseResponse, ErrorDetail
from ..database import db
from ..models.robot import Robot, Position, BatteryStatus, RobotStatus

router = APIRouter(prefix="/api/v1/robots", tags=["robots"])

class Position(BaseModel):
    x: int
    y: int

class Waypoint(BaseModel):
    type: Literal["start", "mid", "end"]
    position: Position

class RouteRequest(BaseModel):
    sequence: int
    waypoints: List[Waypoint]

class RouteResponse(BaseModel):
    routeId: str
    robotId: str
    courseSequence: int
    waypoints: dict
    createdAt: datetime

class MapResponse(BaseModel):
    robotId: str
    mapId: str
    currentLocation: dict
    mapData: dict

class ControlResponse(BaseModel):
    robotId: str
    mode: str
    previousMode: str
    timestamp: datetime
    status: str

class StatusUpdate(BaseModel):
    status: Literal["manual", "auto", "emergency_stop"]

class StatusResponse(BaseModel):
    robotId: str
    status: str
    timestamp: datetime
    location: Position

class LogEntry(BaseModel):
    x: int
    y: int
    timestamp: datetime

class RouteLog(BaseModel):
    routeId: str
    startTime: datetime
    endTime: datetime
    waypoints: List[LogEntry]
    status: str

class DetectionInfo(BaseModel):
    detectionId: str
    timestamp: datetime
    location: Position
    personInfo: dict
    imageUrl: str
    status: str

class LogResponse(BaseModel):
    robotId: str
    routes: Optional[List[RouteLog]] = None
    detections: Optional[List[DetectionInfo]] = None
    pagination: dict

class RobotCreate(BaseModel):
    name: str
    ip_address: str

@router.post("", response_model=BaseResponse[Robot])
async def create_robot(robot_data: RobotCreate):
    try:
        # 자동 증가 ID 생성
        counter = await db.counters.find_one_and_update(
            {"_id": "robot_id"},
            {"$inc": {"seq": 1}},
            return_document=True
        )
        
        robot_id = counter["seq"]
        
        # 기본값이 포함된 전체 로봇 데이터 생성
        robot_dict = {
            "robot_id": robot_id,  # 자동 생성된 ID 사용
            "name": robot_data.name,
            "ip_address": robot_data.ip_address,
            "status": RobotStatus.IDLE,
            "position": {
                "x": 0.0,
                "y": 0.0,
                "theta": 0.0
            },
            "battery": {
                "level": 100.0,
                "is_charging": False
            },
            "last_active": datetime.now(),
            "created_at": datetime.now()
        }
        
        # Robot 모델로 변환하여 유효성 검사
        robot = Robot(**robot_dict)
            
        # MongoDB에 저장
        result = await db.robots.insert_one(robot_dict)
        
        if result.inserted_id:
            return BaseResponse[Robot](
                status=201,
                success=True,
                message="로봇 등록 성공",
                data=robot
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("", response_model=BaseResponse[List[Robot]])
async def get_robots():
    try:
        # MongoDB에서 모든 로봇 정보 조회
        robots = []
        cursor = db.robots.find({})
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            robots.append(Robot(**doc))
            
        return BaseResponse[List[Robot]](
            status=200,
            success=True,
            message="로봇 목록 조회 성공",
            data=robots
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/{id}/routes", response_model=BaseResponse[RouteResponse])
async def set_route(
    id: int = Path(..., description="로봇 ID"),
    request: RouteRequest = None
):
    try:
        return BaseResponse[RouteResponse](
            status=201,
            success=True,
            message="경로 설정 완료",
            data=RouteResponse(
                routeId="route_123",
                robotId=f"robot_{id}",
                courseSequence=request.sequence,
                waypoints={
                    "start": {"x": 100, "y": 200},
                    "mid": {"x": 150, "y": 250},
                    "end": {"x": 200, "y": 300}
                },
                createdAt=datetime.now()
            )
        )
    except Exception:
        return BaseResponse[RouteResponse](
            status=400,
            success=False,
            message="경로 설정 실패",
            errors=[
                ErrorDetail(
                    field="coordinates",
                    message="유효하지 않은 좌표값입니다"
                )
            ]
        )

@router.get("/{id}/map", response_model=BaseResponse[MapResponse])
async def get_map(id: int = Path(..., description="로봇 ID")):
    try:
        return BaseResponse[MapResponse](
            status=200,
            success=True,
            message="로봇 위치 정보 조회 성공",
            data=MapResponse(
                robotId=f"robot_{id}",
                mapId="map_456",
                currentLocation={
                    "x": 150,
                    "y": 200,
                    "timestamp": datetime.now().isoformat()
                },
                mapData={
                    "resolution": 0.05,
                    "width": 1000,
                    "height": 1000,
                    "origin": {"x": 0, "y": 0}
                }
            )
        )
    except Exception:
        return BaseResponse[MapResponse](
            status=404,
            success=False,
            message="맵 정보 조회 실패",
            errors=[
                ErrorDetail(
                    field="robotId",
                    message="해당 로봇을 찾을 수 없습니다"
                )
            ]
        )

@router.post("/{id}/control", response_model=BaseResponse[ControlResponse])
async def control_mode(id: int = Path(..., description="로봇 ID")):
    try:
        return BaseResponse[ControlResponse](
            status=200,
            success=True,
            message="로봇 모드 전환 성공",
            data=ControlResponse(
                robotId=f"robot_{id}",
                mode="manual",
                previousMode="auto",
                timestamp=datetime.now(),
                status="active"
            )
        )
    except Exception:
        return BaseResponse[ControlResponse](
            status=400,
            success=False,
            message="모드 전환 실패",
            errors=[
                ErrorDetail(
                    field="mode",
                    message="현재 상태에서는 모드 전환이 불가능합니다"
                )
            ]
        )

@router.patch("/{id}/status", response_model=BaseResponse[StatusResponse])
async def update_status(
    id: int = Path(..., description="로봇 ID"),
    status: StatusUpdate = None
):
    try:
        return BaseResponse[StatusResponse](
            status=200,
            success=True,
            message="비상 정지 명령 실행 완료",
            data=StatusResponse(
                robotId=f"robot_{id}",
                status="emergency_stopped",
                timestamp=datetime.now(),
                location=Position(x=150, y=200)
            )
        )
    except Exception:
        return BaseResponse[StatusResponse](
            status=500,
            success=False,
            message="비상 정지 실행 실패",
            errors=[
                ErrorDetail(
                    field="system",
                    message="로봇과의 통신이 원활하지 않습니다"
                )
            ]
        )

@router.get("/{id}/logs", response_model=BaseResponse[LogResponse])
async def get_logs(
    id: int = Path(..., description="로봇 ID"),
    type: str = Query(..., description="로그 타입 (route 또는 detection)")
):
    try:
        if type == "route":
            return BaseResponse[LogResponse](
                status=200,
                success=True,
                message="이동 경로 로그 조회 성공",
                data=LogResponse(
                    robotId=f"robot_{id}",
                    routes=[
                        RouteLog(
                            routeId="route_001",
                            startTime=datetime.now(),
                            endTime=datetime.now(),
                            waypoints=[
                                LogEntry(x=100, y=200, timestamp=datetime.now()),
                                LogEntry(x=150, y=250, timestamp=datetime.now())
                            ],
                            status="completed"
                        )
                    ],
                    pagination={
                        "currentPage": 1,
                        "totalPages": 5,
                        "totalItems": 50,
                        "itemsPerPage": 10
                    }
                )
            )
        else:
            return BaseResponse[LogResponse](
                status=200,
                success=True,
                message="인물 감지 로그 조회 성공",
                data=LogResponse(
                    robotId=f"robot_{id}",
                    detections=[
                        DetectionInfo(
                            detectionId="detect_001",
                            timestamp=datetime.now(),
                            location=Position(x=150, y=200),
                            personInfo={
                                "personId": "person_123",
                                "label": "John Doe",
                                "confidence": 0.95
                            },
                            imageUrl="/storage/detections/det_001.jpg",
                            status="verified"
                        )
                    ],
                    pagination={
                        "currentPage": 1,
                        "totalPages": 3,
                        "totalItems": 30,
                        "itemsPerPage": 10
                    }
                )
            )
    except Exception:
        return BaseResponse[LogResponse](
            status=404,
            success=False,
            message="로그 조회 실패",
            errors=[
                ErrorDetail(
                    field="robotId",
                    message="해당 로봇의 로그를 찾을 수 없습니다"
                )
            ]
        ) 