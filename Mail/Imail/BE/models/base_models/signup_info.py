from pydantic import BaseModel, Field

class signUp_Info(BaseModel):
    userName: str
    password: str
    password2: str