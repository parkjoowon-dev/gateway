import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from apps.api import api_app
from apps.auth import auth_app

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from apps.model.User import User
from apps.database import engine, Base, get_db
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(engine)

app = FastAPI()
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/auth', auth_app)
app.mount('/api', api_app)

@app.get('/')
async def root():
    return HTMLResponse('<body>INDEX</body>')



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=3000, reload=True, debug=True)
