from sqlalchemy import Column, Integer, Text
from pydantic import EmailStr

from core.configs import settings

class UserSystemModel(settings.DBBaseModel):
    __tablename__ = 'user_system'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: EmailStr = Column(Text, nullable=False)
    password: str = Column(Text, nullable=False)
    permission_tier: int = Column(Integer, nullable=False)