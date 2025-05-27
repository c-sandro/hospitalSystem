from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from pydantic import EmailStr
import timestamp

from core.configs import settings

from models.blood_type_model import BloodTypeModel

class PatientModel(settings.DBBaseModel):
    __tablename__ = 'patient'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(Text, nullable=False)
    cpf: str = Column(String(11), unique=True, nullable=False)
    birth_date: timestamp = Column(Date, nullable=False)
    sex: str = Column(Boolean, nullable=False)
    phone: str = Column(String(11), nullable=False)
    address: str = Column(Text, nullable=False)
    email: EmailStr = Column(Text)
    blood_type_id: str = Column(Integer, ForeignKey('blood_type.id'))
    allergies: str = Column(Text)
    status: bool = Column(Boolean, nullable=False)

    blood_type = relationship("BloodTypeModel")