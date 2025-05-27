from typing import Optional

import timestamp
from pydantic import BaseModel, EmailStr

class UserSystemSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    password: str
    permission_tier: Optional[int] = None

    class Config:
        orm_mode = True