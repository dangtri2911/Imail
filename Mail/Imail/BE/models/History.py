import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.expression import delete, false, null, true
from sqlalchemy.sql.sqltypes import Date

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from database_connect import Base 
from models.User import User
from models.Email import Email
import datetime

class History(Base):
   __tablename__ = 'History'
   id = Column(Integer, primary_key = True)
   email_id = Column(Integer, ForeignKey(Email.id))
   receiver_id = Column(Integer, ForeignKey(User.id))
   status = Column(Integer,default=0)
   send_date = Column(DateTime, default=datetime.datetime.utcnow)
   # status(0: chưa đọc; 1: dã đọc; 2: đã xóa)