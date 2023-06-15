import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(os.getenv("DATABASE_URL")),
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
