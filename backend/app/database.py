from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings
import logging

settings = get_settings()

# MongoDB 클라이언트 생성
client = AsyncIOMotorClient(
    settings.MONGO_URL,
    serverSelectionTimeoutMS=5000
)

# 데이터베이스 선택
db = client[settings.DATABASE_NAME]

# 컬렉션 정의
robots = db.robots
persons = db.persons
identification_info = db.identification_info
maps = db.maps
routes = db.routes
users = db.users
cctvs = db.cctvs

async def init_db():
    try:
        # 컬렉션 생성
        await db.create_collection("robots")
        await db.create_collection("persons")
        await db.create_collection("identification_info")
        await db.create_collection("maps")
        await db.create_collection("routes")
        await db.create_collection("users")
        await db.create_collection("cctvs")

        # 인덱스 생성
        # robots 컬렉션 인덱스
        await robots.create_index("robot_id", unique=True)
        await robots.create_index([("location.latitude", 1), ("location.longitude", 1)])
        
        # persons 컬렉션 인덱스
        await persons.create_index("person_id", unique=True)
        await persons.create_index("name")
        
        # identification_info 컬렉션 인덱스
        await identification_info.create_index("id_info_id", unique=True)
        await identification_info.create_index("person_id")
        await identification_info.create_index("detect_time")
        
        # maps 컬렉션 인덱스
        await maps.create_index("map_id", unique=True)
        await maps.create_index([("location.latitude", 1), ("location.longitude", 1)])
        
        # routes 컬렉션 인덱스
        await routes.create_index("route_id", unique=True)
        
        # users 컬렉션 인덱스
        await users.create_index("user_id", unique=True)
        await users.create_index("company_seq")
        
        # cctvs 컬렉션 인덱스
        await cctvs.create_index("cctv_id", unique=True)
        await cctvs.create_index([("time_range.start_time", 1), ("time_range.end_time", 1)])

        logging.info("Database initialized successfully")
        return True
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        return False

async def test_connection():
    try:
        await client.admin.command('ping')
        print("MongoDB 연결 성공!")
        # 데이터베이스 초기화
        if await init_db():
            print("데이터베이스 구조 초기화 성공!")
        return True
    except Exception as e:
        print(f"MongoDB 연결 실패: {str(e)}")
        return False 