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
from models.base_models.signin_info import signIn_Info
from database_connect import *


@app.post('/signIn/',response_model= bool)
async def signIn(r: signIn_Info = Depends()):
    query = select([User.id]).where(User.userName == r.userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        query = select([User]).where(and_(User.userName == r.userName))
        result = await database.fetch_one(query)    
        if verifyPassword(r.password,result['password']): 
            return True
        return False
    return False