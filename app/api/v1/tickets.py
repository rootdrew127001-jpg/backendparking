from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List, Optional
from app.db.session import get_session
from app.models.user import User
from app.services.ticket_service import TicketService
from app.models.ticket import Ticket
from app.api.v1.users import get_current_user
from app.schemas.ticket_schema import TicketCreate, TicketRead

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=TicketRead)
def create_ticket(
    plate_no: str,
    vehicle_type: str,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = TicketService(db)
    return service.create_ticket(plate_no, vehicle_type)

@router.post("/{ticket_id}/exit", response_model=TicketCreate)
def exit_ticket(
    ticket_id: int, 
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    service = TicketService(db)
    return service.exit_ticket(ticket_id)

@router.post("/{ticket_id}/pay", response_model=TicketCreate)
def pay_ticket(
    ticket_id: int, db: 
    Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    service = TicketService(db)
    return service.pay_ticket(ticket_id)

@router.get("/")
def list_tickets(
    skip: int = 0,
    limit: int = 10,
    plate_no: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = TicketService(db)
    return service.list_tickets(skip, limit, plate_no, status)