from typing import Optional

import timestamp
from pydantic import BaseModel, EmailStr

class PatientStatusLogSchema(BaseModel):
    id: Optional[int] = None
    date_time: timestamp
    user_system_id: int
    patient_id: int
    reason: str


    class Config:
        orm_mode = True