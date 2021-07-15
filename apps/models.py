from .database import Base
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = "users"
    seq = Column(Integer, primary_key=True, index=True)
    email = Column(String(100))
    password = Column(String(100), nullable=True)
    login_type = Column(String(100))