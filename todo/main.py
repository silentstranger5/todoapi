from fastapi import FastAPI
from . import auth, database, models, permissions, tasks

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(permissions.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    """Root page"""
    return {"message": "Hello World"}
