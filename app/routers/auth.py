from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.utils.security import verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

# Modelo para recibir JSON
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    access_token = create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================
# Registro de usuarios
# ============================================
class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    # Revisar si existe usuario
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = create_access_token({"sub": data.email})  # si usas hashing real, cambia esto

    user = models.User(
        email=data.email,
        password=data.password,  # Asegúrate de usar hashing real si lo deseas
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Usuario registrado con éxito ✔"}
