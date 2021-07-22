import os
from datetime import datetime
from datetime import timedelta

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


# Configuration
API_SECRET_KEY = os.environ.get('API_SECRET_KEY') or None
if API_SECRET_KEY is None:
    raise BaseException('Missing API_SECRET_KEY env var.')
API_ALGORITHM = os.environ.get('API_ALGORITHM') or 'HS256'
API_ACCESS_TOKEN_EXPIRE_MINUTES = cast_to_number('API_ACCESS_TOKEN_EXPIRE_MINUTES') or 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# Token url (We should later create a token url that accepts just a user and a password to use swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


def create_refresh_token(user):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={'seq':user.seq,'email': user.email}, expires_delta=expires)


# Create token for an email
def create_token(user):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'seq':user.seq,'email': user.email}, expires_delta=access_token_expires)
    return access_token


def decode_token(token):
    return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])


async def validate_access_token(token: str = Depends(oauth2_scheme)):
    print("1111111111111")
    try:
        payload = decode_token(token)
        print("222222222222")
        email: str = payload.get('email')
        seq: int = payload.get('seq')
        print("email = " + email)
        print("seq = " + str(seq))
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError as e:
        print(e)
        raise CREDENTIALS_EXCEPTION
    return email

