from pydantic import BaseModel, Field

class signIn_Info(BaseModel):
    userName: str
    password: str
