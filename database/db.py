from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



SQLALCHAMY_DATABASE_URL = "sqlite:///./beautycare.db"
engine = create_engine ((SQLALCHAMY_DATABASE_URL),
          connect_args={"check_same_thread":False} )
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine )
Base=declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()