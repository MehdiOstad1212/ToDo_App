from fastapi import APIRouter, Depends, HTTPException, Path
from tasks.schemas import TaskResponseSchema, TaskCreateSchema, TaskUpdateSchema
from tasks.models import TaskModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter (tags = ["tasks"])

@router.get("/tasks", response_model = List[TaskResponseSchema])
async def retrieve_tasks_list(db: Session = Depends(get_db)):
    result = db.query(TaskModel).all()
    return result

@router.post("/tasks")
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.get("/tasks/{task_id}", response_model = TaskResponseSchema)
async def retrieve_task_detail(task_id: int = Path(..., gt = 0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_obj:
        raise HTTPException(status_code = 404, detail = "Task not found")
    return task_obj

@router.put("/tasks/{task_id}", response_model = TaskResponseSchema)
async def update_task(request: TaskUpdateSchema, task_id: int = Path(..., gt = 0), 
                      db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_obj:
        raise HTTPException(status_code = 404, detail = "Task not found")
    for field, value in request.model_dump(exclude_unset = True).items():
        setattr (task_obj, field, value)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.delete("/tasks/{task_id}", status_code = 204)
async def delete_task(task_id: int = Path(..., gt = 0), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter_by(id = task_id).first()
    if not task_obj:
        raise HTTPException(status_code = 404, detail = "Task not found")
    db.delete(task_obj)
    db.commit()
    