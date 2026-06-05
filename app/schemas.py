from pydantic import BaseModel, __version__ as pydantic_version
from typing import Optional, List

class ClientBase(BaseModel):
    name: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    client_id: str
    created_at: str
    trial_end_date: Optional[str] = None
    class Config:
        if int(pydantic_version.split(".")[0]) >= 2:
            from_attributes = True
        else:
            orm_mode = True

class LeadBase(BaseModel):
    customer_name: str
    customer_phone: str

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    client_id: int
    status: str
    timestamp: str
    class Config:
        if int(pydantic_version.split(".")[0]) >= 2:
            from_attributes = True
        else:
            orm_mode = True

