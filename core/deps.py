from typing import Generator, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, EmailStr

from passlib.context import CryptContext

from core.database import Session
from models.user_system_model import UserSystemModel

class TokenData(BaseModel):
    username: Optional[str] = None

CRYPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_session() -> Generator:
    session: AsyncSession = Session()

    #Abrir e fechar a sessão com o banco de dados
    try:
        yield session
    finally:
        await session.close()

async def authenticate_member(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserSystemModel]:
    async with db as session:
        query = select(UserSystemModel).filter(UserSystemModel.email == email)
        result = await session.execute(query)
        user_system: UserSystemModel = result.scalars().unique().one_or_none()

        if not user_system:
            return None

        if not verify_password(password, user_system.password) or password != user_system.password:
            return None

        return user_system

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return CRYPTO.verify(plain_password, hashed_password)

def generate_password_hash(password: str) -> str:
    return CRYPTO.hash(password)
