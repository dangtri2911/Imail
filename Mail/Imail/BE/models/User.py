import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.expression import delete, false, null, true
from sqlalchemy.sql.sqltypes import Date

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from database_connect import Base 


class User(Base):
   __tablename__ = 'User'
   id = Column(Integer, primary_key = True)
   userName = Column(String)
   password = Column(String)
   fullName = Column(String, default= "")
   birthDay = Column(Date, nullable=true)