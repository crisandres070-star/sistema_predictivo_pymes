from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app import models
from app.utils.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    access_token = create_access_token({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

# ============================
# Registro de usuarios (opcional)
# ============================

class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == data.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed = hash_password(data.password)

    new_user = models.User(email=data.email, password=hashed)
    db.add(new_user)
    db.commit()

    return {"msg": "Usuario registrado correctamente"}
