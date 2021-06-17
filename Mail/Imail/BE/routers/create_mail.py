import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel, Field
from sqlalchemy import insert, update
from sqlalchemy.sql import select
from sqlalchemy import and_  

import os, sys
sys.path.insert(0, os.path.abspath(""))

from models.Email import Email
from models.User import User
from models.base_models.email_info import Email_Info
from database_connect import *



@app.post('/email/createMail/',response_model= int)
async def createMail(r: Email_Info = Depends()):
    query = select([User.id]).where(User.userName == r.userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        stmt = insert(Email).values(sender_id = id_user_["id"] ,content = r.content).returning(Email.id)
        con = engine.connect()
        result = con.execute(stmt)
        for row in result:
            return row['id']
            
    return -1