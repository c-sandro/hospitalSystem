from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import date

class PatientSchema(BaseModel):
    id: Optional[int] = None
    name: str
    cpf: str
    birth_date: date
    sex: bool
    phone: str
    address: str
    email: Optional[EmailStr] = None
    blood_type_id: Optional[int] = None
    allergies: Optional[str] = None
    status: Optional[bool] = None

    class Config:
        orm_mode = True

class PatientSchemaUpdated(PatientSchema):
    name: Optional[str] = None
    cpf: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[bool] = None
    phone: Optional[str] = None
    address: Optional[str] = None