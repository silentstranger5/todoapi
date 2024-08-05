from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    """User Model"""
    id: int
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserInput(BaseModel):
    """User Input Model"""
    username: str
    password: str


class TaskCreate(BaseModel):
    """Task Model for Create Request"""
    name: str


class TaskDelete(BaseModel):
    """Task Model for Delete Request"""
    id: int


class TaskUpdate(BaseModel):
    """Task Model for Update Request"""
    id: int
    name: str | None = None
    complete: bool | None = None


class Permission(BaseModel):
    """Permission Model"""
    task_id: int
    user_id: int
    update: bool = False
    model_config = ConfigDict(from_attributes=True)


class PermissionInput(BaseModel):
    """Permission Input Model"""
    task_id: int
    username: str
    update: bool = False


class Token(BaseModel):
    """Token Model"""
    access_token: str
    token_type: str
