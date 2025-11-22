from pydantic import BaseModel
from datetime import datetime

# ============================
#   USUARIOS
# ============================

class UserBase(BaseModel):
    email: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


# ============================
#   INVENTARIO (BASE)
# ============================

class InventoryItemBase(BaseModel):
    product_name: str
    current_stock: int
    avg_daily_sales: float


# ============================
#   INVENTARIO - RESPUESTA LISTADO
# ============================

class InventoryItemOut(InventoryItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# ============================
#   INVENTARIO - RESPUESTA DE UPLOAD
# ============================

class InventoryUploadResponse(BaseModel):
    message: str


# ============================
#   INVENTARIO - ANÁLISIS PREDICTIVO
# ============================

class InventoryAnalysisItem(BaseModel):
    product_name: str
    current_stock: int
    avg_daily_sales: float
    days_remaining: float
    estimated_out_date: datetime
    risk_level: str

    class Config:
        orm_mode = True
