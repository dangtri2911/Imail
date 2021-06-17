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

@app.post('/mail/DeleteMail/')
async def deleteMail(userName: str, mail_del: int):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        con = engine.connect()
        query = select([Email]).where(Email.id == mail_del)
        mail_ = await database.fetch_one(query)
        if mail_:
            if id_user_['id'] == mail_['sender_id']:
                stmt = delete(History).where(and_(History.email_id == mail_del))
                res = con.execute(stmt)
                stmt = (insert(Trash).values(id= mail_del, sender_id = id_user_['id'], content = mail_['content']))
                res = con.execute(stmt)
                stmt = delete(Email).where(Email.id == mail_del)
                res = con.execute(stmt)
                return True
            else:
                stmt = delete(History).where(and_(History.email_id == mail_del))
                res = con.execute(stmt)
                return True
        return False
    return False 