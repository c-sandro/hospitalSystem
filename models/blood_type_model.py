from sqlalchemy import Column, Integer, String

from core.configs import settings

class BloodTypeModel(settings.DBBaseModel):
    __tablename__ = 'blood_type'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    type: str = Column(String(3), unique=True, nullable=False)