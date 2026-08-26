from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import engine, get_db, Base

# Cria as tabelas no banco (em produção isso seria feito via migrations/Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="API de gerenciamento de tarefas - Projeto DevOps CEUB",
    version="0.1.0",
)


@app.get("/health", tags=["infra"])
def health_check():
    """Endpoint usado pelo pipeline de CI/CD e por ferramentas de monitoramento."""
    return {"status": "ok"}


@app.post("/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@app.get("/tasks", response_model=list[schemas.TaskOut], tags=["tasks"])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_tasks(db, skip=skip, limit=limit)


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut, tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut, tags=["tasks"])
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return None
