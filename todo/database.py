from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from . import config

SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg://"
        f"{config.USER}:{config.PASSWORD}@"
        f"{config.HOST}:{config.PORT}/{config.DBNAME}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
