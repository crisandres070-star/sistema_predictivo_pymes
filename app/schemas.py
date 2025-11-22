from pydantic import BaseModel
from typing import Optional, List

# ======================
# USUARIO
# ======================

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

# ======================
# INVENTARIO
# ======================

class InventoryItemBase(BaseModel):
    name: str
    quantity: int
    price: float

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemOut(InventoryItemBase):
    id: int

    class Config:
        orm_mode = True

# ======================
# ALERTAS
# ======================

class AlertItem(BaseModel):
    name: str
    status: str
    message: str

# ======================
# ANÁLISIS
# ======================

class InventoryAnalysisItem(BaseModel):
    name: str
    stock_status: str
    recommendation: str

class InventoryAnalysisList(BaseModel):
    analysis: List[InventoryAnalysisItem]
