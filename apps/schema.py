from pydantic import BaseModel
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str
    login_type: str