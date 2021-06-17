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

from models.User import User
from models.base_models.signup_info import signUp_Info
from database_connect import *



@app.post('/signUp/',response_model= bool)
async def signUp(r: signUp_Info = Depends()):
    if r.password != r.password2:
        return False
         
    query = select([User.id]).where(User.userName == r.userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        return False

    stmt=insert(User).values(userName = r.userName ,password =hashPassword(r.password))
    con = engine.connect()
    con.execute(stmt)
    return True