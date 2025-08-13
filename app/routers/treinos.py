from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from datetime import date
from ..db import SessionLocal
from ..models import Workout, Pessoa
from ..schemas import WorkoutCreate, WorkoutOut
from ..deps import get_current_user, require_professor

router = APIRouter(prefix="/treinos", tags=["treinos"])

@router.post("", response_model=WorkoutOut, dependencies=[Depends(require_professor)])
def create_workout(body: WorkoutCreate):
    with SessionLocal() as db:
        aluno = db.execute(select(Pessoa).where(Pessoa.email == body.student_email.lower())).scalar_one_or_none()
        if not aluno or aluno.perfil_acesso != "ALUNO":
            raise HTTPException(status_code=400, detail="Aluno inválido.")
        ex_ids = ",".join(map(str, body.exercise_ids)) if body.exercise_ids else None
        obj = Workout(student_email=body.student_email.lower(),
                      workout_name=body.workout_name,
                      creation_date=date.today(),
                      exercise_ids=ex_ids,
                      status="ATIVO")
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return WorkoutOut(id=obj.id, student_email=obj.student_email, workout_name=obj.workout_name,
                          creation_date=obj.creation_date, exercise_ids=obj.exercise_ids, status=obj.status)

@router.get("", response_model=list[WorkoutOut])
def list_workouts(user=Depends(get_current_user)):
    with SessionLocal() as db:
        if user["role"] == "PROFESSOR":
            rows = db.execute(select(Workout)).scalars().all()
        else:
            email = db.execute(select(Pessoa.email).where(Pessoa.id_pessoa == user["sub"])).scalar_one_or_none()
            rows = db.execute(select(Workout).where(Workout.student_email == email, Workout.status == "ATIVO")).scalars().all()

        return [WorkoutOut(id=r.id, student_email=r.student_email, workout_name=r.workout_name,
                           creation_date=r.creation_date, exercise_ids=r.exercise_ids, status=r.status)
                for r in rows]

@router.post("/{workout_id}/clonar", response_model=WorkoutOut, dependencies=[Depends(require_professor)])
def clone_workout(workout_id: str, novo_aluno_email: str):
    with SessionLocal() as db:
        src = db.get(Workout, workout_id)
        if not src:
            raise HTTPException(status_code=404, detail="Treino original não encontrado.")

        aluno = db.execute(select(Pessoa).where(Pessoa.email == novo_aluno_email.lower())).scalar_one_or_none()
        if not aluno or aluno.perfil_acesso != "ALUNO":
            raise HTTPException(status_code=400, detail="Aluno destino inválido.")

        clone = Workout(
            student_email=novo_aluno_email.lower(),
            workout_name=src.workout_name,
            creation_date=date.today(),
            exercise_ids=src.exercise_ids,
            status="ATIVO",
        )
        db.add(clone)
        db.commit()
        db.refresh(clone)

        return WorkoutOut(id=clone.id, student_email=clone.student_email, workout_name=clone.workout_name,
                          creation_date=clone.creation_date, exercise_ids=clone.exercise_ids, status=clone.status)