from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import websocket, robot, control
from .config import get_settings
from .database import test_connection
import asyncio

app = FastAPI()
settings = get_settings()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 도메인을 지정해야 합니다
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

# 라우터 등록
app.include_router(websocket.router)
app.include_router(robot.router)
app.include_router(control.router)

@app.on_event("startup")
async def startup_event():
    # 데이터베이스 연결 테스트
    if not await test_connection():
        print("MongoDB 연결에 실패했습니다. 서버를 종료합니다.")
        exit(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    ) 