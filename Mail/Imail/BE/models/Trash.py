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
import datetime

class Trash(Base):
   __tablename__ = 'Trash'
   id = Column(Integer, primary_key = True)
   sender_id = Column(Integer, ForeignKey(User.id))
   content = Column(String)
   deleted_date = Column(DateTime, default=datetime.datetime.utcnow)   
