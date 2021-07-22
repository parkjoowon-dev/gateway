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

Base.metadata.create_all(engine)

app = FastAPI()
app.mount('/auth', auth_app)
app.mount('/api', api_app)


@app.get('/create')
def create(db:Session = Depends(get_db)):
    
    new_user = User(email="mail4",login_type="google")
    db.add(new_user)
    db.commit()
@app.get('/select')
def select():
    
    user = User.getOrInsertUser("mail1")
    print("user.seq = " + str(user.seq))
    return user
@app.get('/')
async def root():
    return HTMLResponse('<body><a href="/auth/login">Log In</a></body>')


@app.get('/token')
async def token(request: Request):
    return HTMLResponse('''
                <script>
                function send(){
                    var req = new XMLHttpRequest();
                    req.onreadystatechange = function() {
                        if (req.readyState === 4) {
                            console.log(req.response);
                            if (req.response["result"] === true) {
                                window.localStorage.setItem('jwt', req.response["access_token"]);
                                window.localStorage.setItem('refresh', req.response["refresh_token"]);
                            }
                        }
                    }
                    req.withCredentials = true;
                    req.responseType = 'json';
                    req.open("get", "/auth/token?"+window.location.search.substr(1), true);
                    req.send("");

                }
                </script>
                <button onClick="send()">Get FastAPI JWT Token</button>

                <button onClick='fetch("http://127.0.0.1:3000/api/").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Unprotected API
                </button>
                <button onClick='fetch("http://127.0.0.1:3000/api/protected").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API without JWT
                </button>
                <button onClick='fetch("http://127.0.0.1:3000/api/protected",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API wit JWT
                </button>

                <button onClick='fetch("http://127.0.0.1:3000/logout",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{
                    console.log(msg);
                    if (msg["result"] === true) {
                        window.localStorage.removeItem("jwt");
                    }
                    });'>
                Logout
                </button>

                <button onClick='fetch("http://127.0.0.1:3000/auth/refresh",{
                    method: "POST",
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                    body:JSON.stringify({
                        grant_type:\"refresh_token\",
                        refresh_token:window.localStorage.getItem(\"refresh\")
                        })
                }).then((r)=>r.json()).then((msg)=>{
                    console.log(msg);
                    if (msg["result"] === true) {
                        window.localStorage.setItem("jwt", msg["access_token"]);
                    }
                    });'>
                Refresh
                </button>

            ''')


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=3000, reload=True, debug=True)
