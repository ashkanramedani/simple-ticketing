from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, summary="Create a new user", response_description="The created user")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = create_user(db, user)
        logger.info("Created a new user with ID: %s", created_user.id, extra={"user": user.__dict__})
        return created_user
    except ValueError as e:
        logger.error("Failed to create user: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))