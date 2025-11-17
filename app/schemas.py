from pydantic import BaseModel
from datetime import datetime

# -----------------------
# USER SCHEMAS
# -----------------------

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


# -----------------------
# INVENTORY SCHEMAS
# -----------------------

class InventoryItemOut(BaseModel):
    id: int
    product_name: str
    current_stock: float
    avg_daily_sales: float
    created_at: datetime

    class Config:
        orm_mode = True

class InventoryUploadResponse(BaseModel):
    message: str


# -----------------------
# TOKEN SCHEMAS
# -----------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class InventoryAnalysisItem(BaseModel):
    product_name: str
    current_stock: float
    avg_daily_sales: float
    days_remaining: float
    estimated_out_date: datetime
    risk_level: str

    class Config:
        orm_mode = True
