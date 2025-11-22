from pydantic import BaseModel
from datetime import datetime

# ======================================
# USUARIOS
# ======================================
class UserCreate(BaseModel):
    email: str
    password: str
    
class UserOut(BaseModel):
    id: int
    email: str
    
    class Config:
        orm_mode = True


# ======================================
# INVENTARIO
# ======================================
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


# ======================================
# TOKEN
# ======================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    