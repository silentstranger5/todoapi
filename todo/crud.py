from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import auth, models, schemas


def get_user(db: Session, username: str):
    """Get a user from the database"""
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserInput):
    """Add a user to the database"""
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_task_id(db: Session, task_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()


def get_task_author(db: Session, task_id: int, author_id: int):
    return db.query(models.Task).filter(
        and_(models.Task.id == task_id, models.Task.author_id == author_id)
    ).first()


def get_tasks(db: Session, user_id: int):
    """Get all tasks of a user"""
    return db.query(models.Task).join(models.Permission).filter(
        models.Permission.user_id == user_id
    ).all()


def create_task(db: Session, task: schemas.TaskCreate, author_id: int):
    """Add a task to the database"""
    db_task = models.Task(name=task.name, author_id=author_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: schemas.TaskUpdate):
    """Update task in the database"""
    task_dict = task.model_dump(exclude_none=True)
    db.query(models.Task).filter(models.Task.id == task.id).update(task_dict)
    db.commit()


def delete_task(db: Session, task: schemas.TaskDelete):
    """Delete task from the database"""
    db.query(models.Task).filter(models.Task.id == task.id).delete()
    db.commit()


def get_permission(db: Session, permission: schemas.Permission):
    """Get permission from the database"""
    return db.query(models.Permission).filter(
        and_(models.Permission.task_id == permission.task_id, 
             models.Permission.user_id == permission.user_id)
    ).first()


def get_permission_update(db: Session, permission: schemas.Permission):
    """Get permission from the database"""
    return db.query(models.Permission).filter(
        and_(models.Permission.task_id == permission.task_id, 
             models.Permission.user_id == permission.user_id,
             models.Permission.update == True)
    ).first()


def create_permission(db: Session, permission: schemas.Permission):
    """Add a permission to the database"""
    db_permission = models.Permission(**permission.model_dump())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def update_permission(db: Session, permission: schemas.Permission):
    """Update permission in the database"""
    db.query(models.Permission).filter(
        and_(models.Permission.task_id == permission.task_id, 
             models.Permission.user_id == permission.user_id)
    ).update({"update": permission.update})
    db.commit()


def delete_permission(db: Session, permission: schemas.Permission):
    """Delete permission from the database"""
    db.query(models.Permission).filter(
        and_(models.Permission.task_id == permission.task_id, 
             models.Permission.user_id == permission.user_id)
    ).delete()
    db.commit()
