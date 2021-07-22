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


    def getOrInsertUser(email):
        print("getOrInsertUser email = " + email)
        user = User.getUser(email)
        if user == None:
            User.insertUser(email)
            user = User.getUser(email)
            return user
        else:
            return user

    def insertUser(email):
        user = User(email=email)
        db = get_db()
        db.add(user)
        db.commit()
        db.close()
    def getUser(email):
        db = get_db()
        user = None
        try:
            user = db.query(User).filter(User.email == email).one()
        except:
            print("no users")
        finally:
            db.close()
        return user

    def isExist(email, self):
        db = get_db()
        result = False
        try:
            self.getUser(email)
            result = True
        except:
            result = False
        finally:
            db.close()

        return result