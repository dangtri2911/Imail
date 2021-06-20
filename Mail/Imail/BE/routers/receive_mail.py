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

@app.get('/mail/getReceiveMail/')
async def receiveMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)
    if id_user_:
        arrId = list()
        
        stmt = (select([History])).where(History.receiver_id == id_user_['id'])
        result = con.execute(stmt)
        for i in result:
            if not(i['email_id'] in arrId):
                arrId.append(i['email_id']) 
        
        stmt = select([Email,User.userName]).where(and_(Email.id.in_(arrId),Email.sender_id == User.id))
        result = con.execute(stmt)      
        listMail = list()
        for i in result:
            listMail.append(i)

        return listMail
    return False