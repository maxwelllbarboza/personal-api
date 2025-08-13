from fastapi import FastAPI
from sqlalchemy import text
from .db import engine
from .models import Base
from .routers import auth, pessoas, exercicios, treinos

app = FastAPI(title="Personal Trainer API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(pessoas.router)
app.include_router(exercicios.router)
app.include_router(treinos.router)

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}