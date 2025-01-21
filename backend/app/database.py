import motor.motor_asyncio
from .config import get_settings

settings = get_settings()

# MongoDB 클라이언트 생성
client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_URL,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000
)

# 데이터베이스 선택
db = client[settings.DATABASE_NAME]

# 컬렉션 정의
users = db.users
robots = db.robots
camera_logs = db.camera_logs
websocket_logs = db.websocket_logs
sensor_logs = db.sensor_logs

async def test_connection():
    try:
        await client.admin.command('ping')
        print("MongoDB 연결 성공!")
        return True
    except Exception as e:
        print(f"MongoDB 연결 실패: {str(e)}")
        return False 