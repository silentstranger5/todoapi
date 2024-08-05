from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from . import auth, crud, database, schemas

# API Router
router = APIRouter(prefix="/tasks")


@router.get("/get")
async def get_tasks(
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)],
    db: Session = Depends(database.get_db)
):
    """Get Tasks visible for a user"""
    tasks = crud.get_tasks(db, current_user.id)
    return {"tasks": tasks}


@router.post("/create")
async def create_task(
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)],
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db)
):
    """Create a new task"""
    new_task = crud.create_task(db, task, current_user.id)
    new_permission = schemas.Permission(
        task_id=new_task.id, user_id=current_user.id, update=True
    )
    crud.create_permission(db, new_permission)
    return {"message": "Task successfully created"}


@router.post("/update")
async def update_task(
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)],
    task: schemas.TaskUpdate,
    db: Session = Depends(database.get_db)
):
    """Update a task"""
    db_task = crud.get_task_id(db, task.id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist"
        )
    permission_model = schemas.Permission(
        user_id=current_user.id, task_id=task.id
    )
    permission = crud.get_permission_update(db, permission_model)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't have permission to update this task"
        )
    crud.update_task(db, task)
    return {"message": "Task successfully updated"}


@router.post("/delete")
async def delete_task(
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)],
    task: schemas.TaskDelete,
    db: Session = Depends(database.get_db)
):
    """Delete a task"""
    task = crud.get_task_author(db, task.id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task does not exist or you are not it's author"
        )
    crud.delete_task(db, task)
    return {"message": "Task sucessfully deleted"}
