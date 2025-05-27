from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
import timestamp

from core.configs import settings

from models.user_system_model import UserSystemModel
from models.patient_model import PatientModel

class PatientStatusLogModel(settings.DBBaseModel):
    __tablename__ = 'patient_status_log'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    date_time: timestamp = Column(DateTime, nullable=False)
    user_system_id: str = Column(Integer, ForeignKey('user_system.id'), nullable=False)
    patient_id: str = Column(Integer, ForeignKey('patient.id'), nullable=False)
    reason: str = Column(Text, nullable=False)
    new_status: bool = Column(Boolean, nullable=False)

    user_system = relationship("UserSystemModel")
    patient = relationship("PatientModel")