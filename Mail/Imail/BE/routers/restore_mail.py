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

@app.post('/mail/RestoreMail/')
async def restoreMail(userName: str, mail_del: int):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        con = engine.connect()
        query = select([Trash]).where(Trash.id == mail_del)
        mail_ = await database.fetch_one(query)
        if mail_:
            if id_user_['id'] == mail_['sender_id']:
                # stmt = (update(History).where(and_(History.email_id == mail_del)).values(status = 1))
                stmt = insert(Email).values(id = mail_['id'], sender_id = mail_['sender_id'], content = mail_['content'])
                res = con.execute(stmt)
                stmt = (delete(Trash).where(Trash.id == mail_del))
                res = con.execute(stmt)
                return True
            else:
                stmt = (update(History).where(and_(History.email_id == mail_del, History.receiver_id == id_user_['id'], History.status == 2)).values(status = 1))
                res = con.execute(stmt)
                return True
        return False
    return False 