from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketCreate(BaseModel):
    plate_no: str
    vehicle_type: str

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    paid_amount: Optional[float] = None


class TicketRead(BaseModel):
    id: int
    plate_no: str
    vehicle_type: str
    status: str
    time_in: datetime
    time_out: Optional[datetime] = None
    amount: Optional[float] = None

    class Config:
        from_attributes = True 
