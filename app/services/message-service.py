from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate
from fastapi import HTTPException

def create_message(db: Session, ticket_id: int, message: MessageCreate):
    if message.parent_message_id:
        parent = db.query(Message).filter(Message.id == message.parent_message_id, Message.ticket_id == ticket_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent message not found or does not belong to this ticket")
    db_message = Message(**message.dict(), ticket_id=ticket_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message_tree(db: Session, ticket_id: int):
    messages = db.query(Message).filter(Message.ticket_id == ticket_id).all()
    message_dict = {msg.id: msg for msg in messages}
    tree = []

    for msg in messages:
        msg.children = []
        if msg.parent_message_id:
            parent = message_dict.get(msg.parent_message_id)
            if parent:
                parent.children.append(msg)
        else:
            tree.append(msg)

    return tree