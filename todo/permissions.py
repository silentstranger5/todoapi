from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from . import auth, crud, database, schemas

# API router
router = APIRouter(prefix="/permissions")


def validate_transform_permission(
    db: Session,
    permission: schemas.PermissionInput, 
    current_user: schemas.User
):
    user = crud.get_user(db, permission.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    task = crud.get_task_author(db, permission.task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task does not exist or you are not it's author"
        )
    transformed = schemas.Permission(user_id=user.id, task_id=task.id, update=permission.update)
    return transformed


@router.post("/grant")
async def grant_permission(
    permission: schemas.PermissionInput,
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)],
    db: Session = Depends(database.get_db)
):
    """Grant permission for a user"""
    new_permission = validate_transform_permission(db, permission, current_user)
    current_permission = crud.get_permission(db, new_permission)
    if current_permission:
        crud.update_permission(db, new_permission)
    else:
        crud.create_permission(db, new_permission)
    return {"message": "Permission successfully granted"}


@router.post("/revoke")
async def revoke_permission(
    current_user: Annotated[schemas.User, Depends(auth.get_current_user)],
    permission: schemas.PermissionInput,
    db: Session = Depends(database.get_db)
):
    """Revoke permission from a user"""
    new_permission = validate_transform_permission(db, permission, current_user)
    crud.delete_permission(db, new_permission)
    return {"message": "Permission successfully revoked"}
