from pydantic import BaseModel, Field

class Receiver_Info(BaseModel):
    email_id: int
    receiver_name: str