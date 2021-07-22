from fastapi import Depends
from fastapi import FastAPI

from apps.jwt import validate_access_token

api_app = FastAPI()


@api_app.get('/')
def test():
    return {'message': 'unprotected api_app endpoint'}


@api_app.get('/protected')
def test2(current_email: str = Depends(validate_access_token)):
    return {'message': 'protected api_app endpoint'}
