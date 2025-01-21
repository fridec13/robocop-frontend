from fastapi import APIRouter, Path, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..schemas.responses import BaseResponse, ErrorDetail
from ..database import db, persons  # persons 컬렉션 import
import os
import uuid

router = APIRouter(prefix="/api/v1/persons", tags=["persons"])

# 이미지 저장 경로 설정
UPLOAD_DIR = "storage/persons"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ImageInfo(BaseModel):
    imageId: str
    url: str
    uploadedAt: datetime

class PersonResponse(BaseModel):
    personId: str
    label: str
    images: List[ImageInfo]
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

class PersonUpdate(BaseModel):
    person_id: int
    person_label: str

@router.post("", response_model=BaseResponse[PersonResponse])
async def create_person(
    person_id: int = Form(...),
    person_label: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        # 이미지 처리
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise HTTPException(
                status_code=400,
                detail="지원하지 않는 이미지 형식입니다."
            )
        
        image_id = f"person_{person_id}_{uuid.uuid4()}{ext}"
        image_path = os.path.join(UPLOAD_DIR, image_id)
        
        # 파일 저장
        with open(image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        # 데이터베이스에 저장
        person_data = {
            "person_id": f"person_{person_id}",
            "label": person_label,
            "images": [{
                "imageId": image_id,
                "url": f"/storage/persons/{image_id}",
                "uploadedAt": datetime.now()
            }],
            "createdAt": datetime.now()
        }
        
        # persons 컬렉션 사용
        await persons.insert_one(person_data)
        
        return BaseResponse[PersonResponse](
            status=201,
            success=True,
            message="신원 정보 등록 성공",
            data=PersonResponse(**person_data)
        )
    except Exception as e:
        # 이미지가 저장된 경우 삭제
        if 'image_path' in locals():
            try:
                os.remove(image_path)
            except:
                pass
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("", response_model=BaseResponse[List[PersonResponse]])
async def get_persons():
    try:
        return BaseResponse[List[PersonResponse]](
            status=200,
            success=True,
            message="신원 정보 조회 성공",
            data=[
                PersonResponse(
                    personId="person_1",
                    label="Test Person",
                    images=[
                        ImageInfo(
                            imageId="img_001",
                            url="/storage/faces/img_001.jpg",
                            uploadedAt=datetime.now()
                        )
                    ],
                    createdAt=datetime.now()
                )
            ]
        )
    except Exception:
        return BaseResponse[List[PersonResponse]](
            status=404,
            success=False,
            message="신원 정보 조회 실패",
            errors=[
                ErrorDetail(
                    field="database",
                    message="데이터베이스 연결 오류"
                )
            ]
        )

@router.put("/{id}", response_model=BaseResponse[PersonResponse])
async def update_person(
    id: int = Path(..., description="Person ID"),
    person: PersonUpdate = None
):
    try:
        return BaseResponse[PersonResponse](
            status=200,
            success=True,
            message="신원 정보 업데이트 성공",
            data=PersonResponse(
                personId=f"person_{id}",
                label="John Doe Updated",
                images=[
                    ImageInfo(
                        imageId="img_002",
                        url="/storage/faces/img_002.jpg",
                        uploadedAt=datetime.now()
                    )
                ],
                updatedAt=datetime.now()
            )
        )
    except Exception:
        return BaseResponse[PersonResponse](
            status=404,
            success=False,
            message="신원 정보 업데이트 실패",
            errors=[
                ErrorDetail(
                    field="personId",
                    message="해당 사용자를 찾을 수 없습니다"
                )
            ]
        )

@router.delete("/{id}", response_model=BaseResponse[dict])
async def delete_person(id: int = Path(..., description="Person ID")):
    try:
        return BaseResponse[dict](
            status=200,
            success=True,
            message="신원 정보 삭제 완료",
            data={
                "personId": f"person_{id}",
                "deletedAt": datetime.now().isoformat()
            }
        )
    except Exception:
        return BaseResponse[dict](
            status=404,
            success=False,
            message="신원 정보 삭제 실패",
            errors=[
                ErrorDetail(
                    field="personId",
                    message="해당 사용자를 찾을 수 없습니다"
                )
            ]
        ) 