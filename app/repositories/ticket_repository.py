from sqlmodel import Session, select
from typing import Optional, List
from app.models.ticket import Ticket

class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def get(self, ticket_id: int) -> Optional[Ticket]:
        return self.session.get(Ticket, ticket_id)

    def list_all(self) -> List[Ticket]:
        return self.session.exec(select(Ticket)).all()

    def update(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)
        return ticket

    def delete(self, ticket_id: int) -> bool:
        ticket = self.get(ticket_id)
        if not ticket:
            return False
        self.session.delete(ticket)
        self.session.commit()
        return True
