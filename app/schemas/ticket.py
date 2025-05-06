from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.message import MessageResponse
from enum import Enum

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class TicketCreate(BaseModel):
    title: str
    description: Optional[str] = None
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Issue with login",
                "description": "Cannot log in to the system",
                "user_id": 1
            }
        }

class TicketUpdate(BaseModel):
    status: TicketStatus

    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_progress"
            }
        }

class TicketResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    user_id: int
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Issue with login",
                "description": "Cannot log in to the system",
                "status": "open",
                "created_at": "2025-05-05T10:00:00",
                "updated_at": "2025-05-05T10:00:00",
                "user_id": 1,
                "messages": []
            }
        }

class TicketListResponse(BaseModel):
    id: int
    title: str
    status: TicketStatus

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Issue with login",
                "status": "open"
            }
        }