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

@app.get('/mail/getUnreadMail/')
async def getUnReadMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_curr_ = await database.fetch_one(query)

    if id_curr_:
        stmt = (select([History]).where(and_(History.status == 0, History.receiver_id == id_curr_['id'])))
        res = con.execute(stmt)
        
        arrId = list()
        for i in res:
            if not(i['email_id'] in arrId):
                arrId.append(i['email_id'])  

        stmt = select([Email,User]).where(and_(Email.id.in_(arrId),User.id == Email.sender_id))
        result = con.execute(stmt)

        listMail = list()
        
        for i in result:
            listMail.append(i)
        
        return listMail

    return null