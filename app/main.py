from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, users, inventory
from . import models

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SaaS Predictivo PYMES")

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(inventory.router)

@app.get("/")
def root():
    return {"message": "API SaaS Predictivo PYMES funcionando 🚀"}
