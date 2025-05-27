from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import timestamp

from core.configs import settings

from models.patient_model import PatientModel
from models.doctor_model import DoctorModel

class AppointmentModel(settings.DBBaseModel):
    __tablename__ = 'appointment'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    patient_id: str = Column(Integer, ForeignKey('patient.id'), nullable=False)
    doctor_id: str = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    date_time: timestamp = Column(DateTime, nullable=False)

    patient = relationship("PatientModel")
    doctor = relationship("DoctorModel")