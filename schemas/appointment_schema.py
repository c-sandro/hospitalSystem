from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class AppointmentSchema(BaseModel):
    id: Optional[int] = None
    patient_id: int
    doctor_id: int
    date_time: datetime

    class Config:
        orm_mode = True