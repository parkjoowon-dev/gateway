from fastapi import Depends
from fastapi import FastAPI
from sqlalchemy.orm import Session
from apps.model.User import User
from apps.database import engine, Base, get_db
from apps.jwt import validate_access_token

api_app = FastAPI()


@api_app.get('/')
def test():
    return {'message': 'unprotected api_app endpoint'}


@api_app.get('/protected')
def test2(current_email: str = Depends(validate_access_token)):
    return {'message': 'protected api_app endpoint'}
    
@api_app.get('/create')
def create(db:Session = Depends(get_db)):
    
    new_user = User(email="mail4",login_type="google")
    db.add(new_user)
    db.commit()
@api_app.get('/select')
def select():
    user = User.getOrInsertUser("mail1")
    print("user.seq = " + str(user.seq))
    return user