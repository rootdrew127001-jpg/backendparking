from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.session import get_session
from app.services.ticket_service import TicketService
from app.models.ticket import Ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=Ticket)
def create_ticket(
    plate_no: str,
    vehicle_type: str,
    db: Session = Depends(get_session)
):
    service = TicketService(db)
    return service.create_ticket(plate_no, vehicle_type)

@router.post("/{ticket_id}/exit", response_model=Ticket)
def exit_ticket(ticket_id: int, db: Session = Depends(get_session)):
    service = TicketService(db)
    return service.exit_ticket(ticket_id)

@router.post("/{ticket_id}/pay", response_model=Ticket)
def pay_ticket(ticket_id: int, db: Session = Depends(get_session)):
    service = TicketService(db)
    return service.pay_ticket(ticket_id)

@router.get("/", response_model=List[Ticket])
def list_tickets(db: Session = Depends(get_session)):
    service = TicketService(db)
    return service.list_tickets()