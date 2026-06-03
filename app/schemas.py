from pydantic import BaseModel, __version__ as pydantic_version

class LeadBase(BaseModel):
    customer_name: str
    customer_phone: str

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    status: str
    timestamp: str
    class Config:
        if int(pydantic_version.split(".")[0]) >= 2:
            from_attributes = True
        else:
            orm_mode = True
