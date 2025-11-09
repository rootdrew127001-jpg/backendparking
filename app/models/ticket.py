from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: Optional[int] = Field(default=None, primary_key=True)
    plate_no: str = Field(index=True)
    vehicle_type: str = Field(index=True)
    time_in: datetime = Field(default_factory=datetime.utcnow)
    time_out: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    fee: float = 0.0
    status: str = Field(default="OPEN")
