from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel

T = TypeVar('T')

class ErrorDetail(BaseModel):
    field: str
    message: str

class BaseResponse(BaseModel, Generic[T]):
    status: int
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[List[ErrorDetail]] = None 