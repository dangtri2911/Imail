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

@app.get('/mail/getAll/')
async def AllMail():
    con = engine.connect()
    stmt = (select([Email]))
    result = con.execute(stmt)

    listMail = list()
    for i in result:
        listMail.append(i)
    return listMail