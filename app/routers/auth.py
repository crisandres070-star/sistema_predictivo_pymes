from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.utils.security import verify_password, hash_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

# ================================
# LOGIN
# ================================
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ================================
# REGISTRO DE USUARIOS
# ================================
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    hashed = hash_password(data.password)

    user = models.User(email=data.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Usuario creado con éxito"}
