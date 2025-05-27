from sqlalchemy import Column, Integer, String, Text, Time
from pydantic import EmailStr
import timestamp

from core.configs import settings

class DoctorModel(settings.DBBaseModel):
    __tablename__ = 'doctor'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(Text, nullable=False)
    cpf: str = Column(String(11), nullable=False, unique=True)
    crm: int = Column(Integer, nullable=False, unique=True)
    phone: str = Column(String(11), nullable=False)
    email: EmailStr = Column(Text)
    shift_start: timestamp = Column(Time, nullable=False)
    shift_finish: timestamp = Column(Time, nullable=False)