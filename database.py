import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 요청마다 DB 세션을 열고, 끝나면 닫아주는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()