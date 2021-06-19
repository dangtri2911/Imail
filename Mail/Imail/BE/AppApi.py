import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# import os, sys
# sys.path.insert(0, os.path.abspath("."))
from database_connect import *
from database_connect import Base
from routers.sign_up import signUp
from routers.sign_in import signIn
from routers.create_mail import createMail
from routers.add_receiver import addReceiver
from routers.read_mail import readMail
from routers.get_unread_mail import getUnReadMail
from routers.get_sent_mail import getSentMail
from routers.get_deleted_mail import getDeletedMail
from routers.delete_mail import deleteMail
from routers.restore_mail import restoreMail
from routers.get_all import AllMail
from routers.get_normal_mail import getNormalMail
from routers.receive_mail import receiveMail
from routers.user_info import updateInfo

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    uvicorn.run("database_connect:app", host="0.0.0.0", port=3000, reload=True)

# Máy đang lag a oi :>