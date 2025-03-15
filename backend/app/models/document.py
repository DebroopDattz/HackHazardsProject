from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class Document(BaseModel):
    id: str
    title: str
    content: str
    classification_level: str
    department: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    metadata: dict
    version: int
    is_encrypted: bool
    access_control_list: List[str]
    retention_period: Optional[int]
    digital_signature: Optional[str] 