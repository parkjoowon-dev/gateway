
import os
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse

from starlette.config import Config
from apps.jwt import CREDENTIALS_EXCEPTION


# Create the auth app
google_oauth2_app = FastAPI()

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Frontend URL:
GOOGLE_REDIRECT_URL = os.environ.get('GOOGLE_REDIRECT_URL') or 'http://127.0.0.1:3000/auth/google_oauth2/callback'
# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
async def google_get_email(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise CREDENTIALS_EXCEPTION
    user_data = await oauth.google.parse_id_token(request, access_token)
    return user_data['email']

@google_oauth2_app.route('/')
async def login(request: Request):
    redirect_uri = GOOGLE_REDIRECT_URL  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)
@google_oauth2_app.get('/callback')
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
                send();
                </script>
            ''')