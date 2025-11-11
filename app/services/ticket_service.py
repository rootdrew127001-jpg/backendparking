from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository

class TicketService:
    def __init__(self, db: Session):
        self.repo = TicketRepository(db)

    def create_ticket(self, plate_no: str, vehicle_type: str) -> Ticket:
        ticket = Ticket(plate_no=plate_no, vehicle_type=vehicle_type)
        return self.repo.create(ticket)

    def exit_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.repo.get(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        if ticket.time_out:
            raise HTTPException(status_code=400, detail="Already exited")

        ticket.time_out = datetime.utcnow()
        delta = ticket.time_out - ticket.time_in
        ticket.duration_minutes = int(delta.total_seconds() / 60)

        hours = max(1, ticket.duration_minutes // 60)
        ticket.fee = 20 + (10 * hours)
        ticket.status = "PENDING_PAYMENT"

        return self.repo.update(ticket)

    def pay_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.repo.get(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        if ticket.status == "PAID":
            raise HTTPException(status_code=400, detail="Already paid")

        ticket.status = "PAID"
        return self.repo.update(ticket)

    def list_tickets(self):
        return self.repo.list_all()
    

    def list_tickets(
        self,
        skip: int = 0,
        limit: int = 10,
        plate_no: Optional[str] = None,
        status: Optional[str] = None
    ):
        items = self.repo.list_tickets(skip, limit, plate_no, status)
        total = self.repo.count_tickets(plate_no, status)
        return {
            "total": total,
            "page": (skip // limit) + 1,
            "size": limit,
            "items": items
        }
