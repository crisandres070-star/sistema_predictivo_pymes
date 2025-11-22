from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "MEGASECRETO123456789"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================
# HASHING DE CONTRASEÑAS
# ============================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ============================
# GENERAR TOKEN JWT
# ============================

def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ============================
# DECODIFICAR TOKEN
# ============================

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None
