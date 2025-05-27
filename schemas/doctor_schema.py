from typing import Optional

import timestamp
from pydantic import BaseModel, EmailStr

class PatientSchema(BaseModel):
    id: Optional[int] = None
    name: str
    cpf: str
    crm: int
    phone: str
    email: Optional[EmailStr] = None
    shift_start: timestamp
    shift_finish: timestamp


    class Config:
        orm_mode = True