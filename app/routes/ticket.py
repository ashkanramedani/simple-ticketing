from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate, TicketListResponse
from app.schemas.message import MessageCreate, MessageResponse
from app.services.ticket_service import create_ticket, get_ticket, update_ticket, get_tickets
from app.services.message_service import create_message, get_message_tree
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketResponse, summary="Create a new ticket", response_description="The created ticket")
def create_new_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket = create_ticket(db, ticket)
    logger.info("Created a new ticket with ID: %s", ticket.id, extra={"ticket": ticket.__dict__})
    return ticket

@router.get("/{ticket_id}", response_model=TicketResponse, summary="Get ticket details", response_description="Ticket details with tree-structured messages")
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        logger.warning("Ticket with ID %s not found", ticket_id)
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.messages = get_message_tree(db, ticket_id)
    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse, summary="Update ticket status", response_description="The updated ticket")
def update_ticket_status(ticket_id: int, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    ticket = update_ticket(db, ticket_id, ticket_update)
    if not ticket:
        logger.warning("Ticket with ID %s not found for update", ticket_id)
        raise HTTPException(status_code=404, detail="Ticket not found")
    logger.info("Updated ticket with ID: %s", ticket_id, extra={"ticket": ticket.__dict__})
    return ticket

@router.get("/", response_model=List[TicketListResponse], summary="List tickets", response_description="List of tickets with pagination and filters")
def read_tickets(
    skip: int = Query(0, ge=0, description="Number of tickets to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of tickets to return"),
    status: str = Query(None, description="Filter by ticket status (open, in_progress, closed)"),
    user_id: int = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db)
):
    tickets = get_tickets(db, skip, limit, status, user_id)
    return tickets

@router.post("/{ticket_id}/messages/", response_model=MessageResponse, summary="Create a message", response_description="The created message")
def create_new_message(ticket_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    message = create_message(db, ticket_id, message)
    logger.info("Created a new message with ID %s for ticket %s", message.id, ticket_id)
    return message