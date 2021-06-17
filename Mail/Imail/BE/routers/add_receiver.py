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
from models.base_models.receiver_info import Receiver_Info
from database_connect import *



@app.post('/email/addReceiver/',response_model= bool)
async def addReceiver(r: Receiver_Info = Depends()):

    query = select([User.id]).where(User.userName == r.receiver_name)
    id_recei_ = await database.fetch_one(query)

    if id_recei_:
        stmt = insert(History).values(email_id = r.email_id ,receiver_id = id_recei_["id"])
        con = engine.connect()
        con.execute(stmt)
        return True
    return False