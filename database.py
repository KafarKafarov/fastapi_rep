from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DATABASE_URL

URL_DATABASE = DATABASE_URL
class Base(DeclarativeBase):
    pass
engine = create_engine(URL_DATABASE, echo=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
