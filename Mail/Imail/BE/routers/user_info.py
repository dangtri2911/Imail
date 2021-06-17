import sqlalchemy
from sqlalchemy.sql.expression import null
import databases
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel, Field
from sqlalchemy import insert, update
from sqlalchemy.sql import select
from sqlalchemy import and_  
from sqlalchemy.sql.expression import delete, false, null, true

import os, sys
sys.path.insert(0, os.path.abspath(""))

from models.History import History
from models.User import User
from models.Email import Email
from models.Trash import Trash
from database_connect import *
import datetime

@app.post('/user/UserInfo/')
async def updateInfo(userName: str,
                        new_fullName: str,
                        new_birthDay: datetime.date
                        ):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)
    if id_user_:
        stmt = update(User).where(User.id == id_user_['id']).values(fullName = new_fullName, birthDay = new_birthDay)
        result = con.execute(stmt)
        return True
    return False