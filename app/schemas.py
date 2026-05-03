from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    kyc_status: str = "PENDING"

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    email: str
    phone: str
    kyc_status: str

    class Config:
        from_attributes = True
