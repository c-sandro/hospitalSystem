from typing import ClassVar
from sqlalchemy.ext.declarative import declarative_base

from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DB_URL: str = "postgresql+asyncpg://hospitaldbmanager:QcySaDbWczNupvvl@localhost:5432/hospitalDB"

    API_V1_STR: str = "/api/v1"

    DBBaseModel: ClassVar = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()