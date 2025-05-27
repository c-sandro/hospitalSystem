from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
import timestamp

from core.configs import settings

from models.user_system_model import UserSystemModel
from models.patient_model import PatientModel

class PatientEditLogModel(settings.DBBaseModel):
    __tablename__ = 'patient_edit_log'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    date_time: timestamp = Column(DateTime, nullable=False)
    user_system_id: str = Column(Integer, ForeignKey('user_system.id'), nullable=False)
    patient_id: str = Column(Integer, ForeignKey('patient.id'), nullable=False)
    changes: str = Column(Text, nullable=False)

    user_system = relationship("UserSystemModel")
    patient = relationship("PatientModel")