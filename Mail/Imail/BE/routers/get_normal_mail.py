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

@app.get('/mail/getNormalMail/')
async def getNormalMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)
    if id_user_:
        stmt = (select([Email])).where(Email.sender_id == id_user_['id'])
        result = con.execute(stmt)
        
        arrId = set()
        for i in result:
            if not(i['id'] in arrId):
                arrId.add(i['id'])  
        
        stmt = (select([History])).where(History.receiver_id == id_user_['id'])
        result = con.execute(stmt)
        for i in result:
            if not(i['receiver_id'] in arrId):
                arrId.add(i['receiver_id']) 
        
        stmt = select([Email,User.userName]).where(and_(Email.id.in_(arrId),Email.sender_id == User.id))
        result = con.execute(stmt)
        listMail = list()
        for i in result:
            listMail.append(i)

        return listMail
    return False