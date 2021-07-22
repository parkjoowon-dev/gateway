import os
from datetime import datetime


from fastapi import FastAPI, Depends
from fastapi import Request
from fastapi.responses import HTMLResponse

from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from apps.oauth.google_oauth2 import google_oauth2_app, google_get_email

from apps.jwt import create_refresh_token, create_token, CREDENTIALS_EXCEPTION, decode_token
from apps.model.User import User
from apps.database import SessionLocal, engine, Base, get_db
from sqlalchemy.orm import Session

# Create the auth app
auth_app = FastAPI()
auth_app.mount('/google_oauth2', google_oauth2_app)

# Set up the middleware to read the request session
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
auth_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)






@auth_app.get('/token')
async def auth(request: Request):
    print("1111111")
    email = await google_get_email(request)
    print("22222222")
    user = User.getOrInsertUser(email)
    return JSONResponse({
        'result': True,
        'access_token': create_token(user),
        'refresh_token': create_refresh_token(user),
    })


@auth_app.post('/refresh')
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == 'POST':
            form = await request.json()
            if form.get('grant_type') == 'refresh_token':
                token = form.get('refresh_token')
                payload = decode_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                    email = payload.get('email')
                    user = User.getUser(email)
                    return JSONResponse({'result': True, 'access_token': create_token(user)})

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION
