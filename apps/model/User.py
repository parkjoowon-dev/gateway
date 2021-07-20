from apps.database import Base
from sqlalchemy import Column, Integer, String
from fastapi import Depends
from sqlalchemy.orm import Session
from apps.database import get_db
class User(Base):
    __tablename__ = "users"
    seq = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100))
    login_type = Column(String(100))

    def isExist(db, email):
        try:
            db.query(User).filter(User.email == email).one()
            return True
        except:
            return False