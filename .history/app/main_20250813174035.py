from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import db, models
from .db import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API Personal Trainer Online"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.Pessoa).all()
