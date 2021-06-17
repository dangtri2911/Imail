import sqlalchemy
from sqlalchemy.sql.expression import null
import databases
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel, Field
from sqlalchemy import insert, update
from sqlalchemy.sql import select
from sqlalchemy import and_  

import os, sys
sys.path.insert(0, os.path.abspath(""))

from models.History import History
from models.User import User
from models.Email import Email
from database_connect import *

@app.get('/mail/getSentMail/')
async def getSentMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_recei_ = await database.fetch_one(query)

    if id_recei_:
        stmt = select([Email,User]).where(and_(Email.sender_id == id_recei_['id'],Email.sender_id == User.id))
        result = con.execute(stmt)
        listMail = list()
        for i in result:
            listMail.append(i)
        return listMail
    return null
