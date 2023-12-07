from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import get_settings
from dotenv import load_dotenv
import os

settings = get_settings()

load_dotenv()

SQLALCHEMY_DATABASE_URI = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://127.0.0.1:5432/FastAPI 2?user=postgres&password=designate9319'
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# SQLALCHEMY_DATABASE_URI = 'sqlite:///./app.db'

# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()