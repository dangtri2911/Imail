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

from models.History import History
from models.User import User
from models.Email import Email
from models.base_models.receiver_info import Receiver_Info
from database_connect import *

@app.get('/mail/readMail/')
async def readMail(userName: str, mail_read: int):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_curr_ = await database.fetch_one(query)
    query = select([Email]).where(Email.id == mail_read)
    sender_id = await database.fetch_one(query)

    if id_curr_:
        if id_curr_['id'] != sender_id['id']:
            # update to read
            stmt = (update(History).where(and_(History.email_id == mail_read, History.receiver_id == id_curr_['id'], History.status == 0)).values(status = 1))
            res = con.execute(stmt)
            return True
        else:
            return True
    return False