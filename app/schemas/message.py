from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageCreate(BaseModel):
    content: str
    user_id: int
    parent_message_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Please provide more details",
                "user_id": 1,
                "parent_message_id": None
            }
        }

class MessageResponse(BaseModel):
    id: int
    content: str
    ticket_id: int
    user_id: int
    parent_message_id: Optional[int]
    created_at: datetime
    children: List["MessageResponse"] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "content": "Please provide more details",
                "ticket_id": 1,
                "user_id": 1,
                "parent_message_id": None,
                "created_at": "2025-05-05T10:05:00",
                "children": []
            }
        }