from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository

router = APIRouter(prefix="/tickets-test", tags=["tickets-test"])

@router.post("/")
def create_ticket(db: Session = Depends(get_session)):
    repo = TicketRepository(db)
    ticket = Ticket(plate_no="ABC123", vehicle_type="CAR")
    return repo.create(ticket)

@router.get("/")
def list_tickets(db: Session = Depends(get_session)):
    repo = TicketRepository(db)
    return repo.list_all()
