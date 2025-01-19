from database import SessionLocal
from models import User
from auth import get_password_hash

def create_initial_admin():
    db = SessionLocal()
    
    # 관리자 계정이 이미 존재하는지 확인
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        print("Admin account already exists")
        return
    
    # 새 관리자 계정 생성
    admin_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),  # 실제 운영환경에서는 더 강력한 비밀번호 사용
        is_active=True,
        is_admin=True
    )
    
    db.add(admin_user)
    db.commit()
    print("Admin account created successfully")

if __name__ == "__main__":
    create_initial_admin() 