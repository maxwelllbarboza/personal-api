from fastapi import APIRouter, Depends
from sqlalchemy import select
from ..db import SessionLocal
from ..models import Exercise
from ..schemas import ExerciseCreate, ExerciseOut
from ..deps import require_professor

router = APIRouter(prefix="/exercicios", tags=["exercicios"])

@router.post("", response_model=ExerciseOut, dependencies=[Depends(require_professor)])
def create_exercise(body: ExerciseCreate):
    with SessionLocal() as db:
        obj = Exercise(category=body.category, name=body.name, image=body.image)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return ExerciseOut(id=obj.id, category=obj.category, name=obj.name, image=obj.image)

@router.get("", response_model=list[ExerciseOut])
def list_exercises():
    with SessionLocal() as db:
        rows = db.execute(select(Exercise)).scalars().all()
        return [ExerciseOut(id=r.id, category=r.category, name=r.name, image=r.image) for r in rows]