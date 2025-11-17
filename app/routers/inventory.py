from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from fastapi.security import OAuth2PasswordBearer
from ..database import SessionLocal
from .. import models, schemas
from ..utils.security import decode_access_token

router = APIRouter(prefix="/inventory", tags=["Inventory"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

@router.post("/upload", response_model=schemas.InventoryUploadResponse)
async def upload_inventory(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    df = pd.read_excel(file.file)

    required_cols = {"product_name", "current_stock", "avg_daily_sales"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(status_code=400, detail="El Excel no tiene las columnas necesarias")

    for _, row in df.iterrows():
        item = models.InventoryItem(
            user_id=current_user.id,
            product_name=row["product_name"],
            current_stock=row["current_stock"],
            avg_daily_sales=row["avg_daily_sales"],
        )
        db.add(item)

    db.commit()
    return {"message": "Inventario guardado con éxito 🚀"}
# ================================
#  LISTAR INVENTARIO DEL USUARIO
# ================================

@router.get("/list", response_model=list[schemas.InventoryItemOut])
async def list_inventory(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    items = db.query(models.InventoryItem).filter(models.InventoryItem.user_id == current_user.id).all()
    return items

# =====================================
#   ANALISIS PREDICTIVO DE INVENTARIO
# =====================================

@router.get("/analysis", response_model=list[schemas.InventoryAnalysisItem])
async def inventory_analysis(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    from datetime import datetime, timedelta

    items = db.query(models.InventoryItem).filter(models.InventoryItem.user_id == current_user.id).all()
    results = []

    for item in items:
        if item.avg_daily_sales > 0:
            days_remaining = item.current_stock / item.avg_daily_sales
        else:
            days_remaining = 9999  # no se vende nada

        estimated_out = datetime.now() + timedelta(days=days_remaining)

        # Nivel de riesgo
        if days_remaining <= 3:
            risk = "CRÍTICO"
        elif days_remaining <= 7:
            risk = "MEDIO"
        else:
            risk = "NORMAL"

        results.append({
            "product_name": item.product_name,
            "current_stock": item.current_stock,
            "avg_daily_sales": item.avg_daily_sales,
            "days_remaining": round(days_remaining, 1),
            "estimated_out_date": estimated_out,
            "risk_level": risk
        })

    return results
# =====================================
#      ALERTAS AUTOMÁTICAS DE STOCK
# =====================================

@router.get("/alerts")
async def inventory_alerts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    from datetime import datetime, timedelta

    items = db.query(models.InventoryItem).filter(models.InventoryItem.user_id == current_user.id).all()
    alerts = []

    for item in items:
        # Si no hay ventas, es sin rotación
        if item.avg_daily_sales == 0:
            alerts.append({
                "product_name": item.product_name,
                "alert": "SIN ROTACIÓN",
                "detail": "Este producto no tiene ventas registradas"
            })
            continue

        # Calcular días restantes
        days_remaining = item.current_stock / item.avg_daily_sales
        estimated_out = datetime.now() + timedelta(days=days_remaining)

        # ALERTAS
        if days_remaining <= 0:
            alerts.append({
                "product_name": item.product_name,
                "alert": "AGOTADO",
                "detail": "Este producto ya no tiene stock"
            })
        elif days_remaining <= 3:
            alerts.append({
                "product_name": item.product_name,
                "alert": "CRÍTICO",
                "detail": f"Quedan {round(days_remaining,1)} días de stock"
            })
        elif days_remaining <= 7:
            alerts.append({
                "product_name": item.product_name,
                "alert": "ADVERTENCIA",
                "detail": f"Quedan {round(days_remaining,1)} días de stock"
            })

    return alerts
