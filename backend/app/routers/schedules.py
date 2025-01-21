from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime
from ..schemas.responses import BaseResponse, ErrorDetail

router = APIRouter(prefix="/api/v1/schedules", tags=["schedules"])

class Time(BaseModel):
    hour: int
    minute: int

class Schedule(BaseModel):
    time: Time
    days: List[Literal["sun", "mon", "tue", "wed", "thu", "fri", "sat"]]

class ScheduleRequest(BaseModel):
    robotId: int
    schedule: Schedule

class ScheduleResponse(BaseModel):
    scheduleId: str
    time: Time
    days: List[str]
    createdAt: datetime

@router.post("", response_model=BaseResponse[ScheduleResponse])
async def create_schedule(request: ScheduleRequest):
    try:
        # TODO: 실제 스케줄 저장 로직 구현
        return BaseResponse[ScheduleResponse](
            status=201,
            success=True,
            message="경비 스케줄 설정 완료",
            data=ScheduleResponse(
                scheduleId="12345",
                time=request.schedule.time,
                days=request.schedule.days,
                createdAt=datetime.now()
            )
        )
    except Exception:
        return BaseResponse[ScheduleResponse](
            status=400,
            success=False,
            message="스케줄 설정 실패",
            errors=[
                ErrorDetail(
                    field="time",
                    message="유효하지 않은 시간 형식입니다"
                ),
                ErrorDetail(
                    field="days",
                    message="최소 하나의 요일을 선택해야 합니다"
                )
            ]
        ) 