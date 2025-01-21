# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from ..core.security import (
    SECRET_KEY,
    ALGORITHM,
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash
)
from ..database import db
from ..models.user import Token, User
from datetime import datetime

router = APIRouter()

# 초기 관리자 계정 생성 함수
async def create_admin_user():
    # 관리자 계정이 없는 경우에만 생성
    if not await db.users.find_one({"username": "admin"}):
        admin_user = {
            "username": "admin",
            "password": get_password_hash("admin"),
            "role": "admin",
            "is_active": True,
            "created_at": datetime.now()
        }
        await db.users.insert_one(admin_user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 사용자 확인
    user = await db.users.find_one({"username": form_data.username})
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 토큰 생성
    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    refresh_token = create_refresh_token(
        data={"sub": user["username"]}
    )

    # Refresh 토큰을 DB에 저장하고 last_login 업데이트
    await db.users.update_one(
        {"username": user["username"]},
        {
            "$set": {
                "refresh_token": refresh_token,
                "last_login": datetime.now(),
                "updated_at": datetime.now()
            }
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(current_token: str):
    try:
        # Refresh 토큰 검증
        payload = jwt.decode(current_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # DB에서 사용자의 refresh 토큰 확인
        user = await db.users.find_one({"username": username})
        if not user or user.get("refresh_token") != current_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # 새로운 토큰 생성
        new_access_token = create_access_token(data={"sub": username})
        new_refresh_token = create_refresh_token(data={"sub": username})

        # 새로운 refresh 토큰을 DB에 저장
        await db.users.update_one(
            {"username": username},
            {
                "$set": {
                    "refresh_token": new_refresh_token,
                    "updated_at": datetime.now()
                }
            }
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )