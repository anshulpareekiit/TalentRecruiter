from typing import Any, Optional, Dict
from pydantic import BaseModel
from fastapi import status

class ResponseSchema(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    status_code: int
