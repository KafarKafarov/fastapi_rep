from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

URL_DATABASE = DATABASE_URL
Base = declarative_base()
engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
