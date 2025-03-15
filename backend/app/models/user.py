from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str
    department: str
    role: str
    clearance_level: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime
    permissions: List[str]
    two_factor_enabled: bool 