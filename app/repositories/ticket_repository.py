from sqlmodel import Session, select
from typing import Optional, List
from app.models.ticket import Ticket

class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_tickets(
        self,
        skip: int = 0,
        limit: int = 10,
        plate_no: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Ticket]:
        query = select(Ticket)

        if plate_no:
            query = query.where(Ticket.plate_no.contains(plate_no))
        if status:
            query = query.where(Ticket.status == status)

        result = self.session.exec(query.offset(skip).limit(limit))
        return result.all()

    def count_tickets(self, plate_no: Optional[str] = None, status: Optional[str] = None) -> int:
        query = select(Ticket)
        if plate_no:
            query = query.where(Ticket.plate_no.contains(plate_no))
        if status:
            query = query.where(Ticket.status == status)
        return len(self.session.exec(query).all())
