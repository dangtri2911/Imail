from pydantic import BaseModel, Field

class Email_Info(BaseModel):
    userName: str
    content: str