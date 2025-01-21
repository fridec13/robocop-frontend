from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, schedules, robots, persons
from .database import test_connection
import uvicorn


from fastapi import FastAPI
from .database import test_connection
from .routers.auth import create_admin_user

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await test_connection()
    await create_admin_user()

# 라우터 등록
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])

app = FastAPI(title="Robot Management API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin을 지정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(schedules.router)
app.include_router(robots.router)
app.include_router(persons.router)

@app.get("/")
async def root():
    return {"message": "Robot Management API"}

@app.on_event("startup")
async def startup_event():
    # MongoDB 연결 테스트
    if not await test_connection():
        import sys
        sys.exit(1)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 