from sqlalchemy.sql.expression import delete, false, null, true
from sqlalchemy.sql.sqltypes import Date
from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Boolean, DateTime
from pydantic import BaseModel, Field
from sqlalchemy import insert, update
from sqlalchemy.sql import select
from sqlalchemy import and_  
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import datetime

app = FastAPI()

# Handle CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = "postgresql://postgres:tri29112001@localhost/demo"

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

Base = declarative_base()

# demo = sqlalchemy.Table(
#     "Tri",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("name", sqlalchemy.String(100))
# )


engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

# Create Table
class User(Base):
   __tablename__ = 'User'
   id = Column(Integer, primary_key = True)
   userName = Column(String)
   password = Column(String)
   fullName = Column(String, default= "")
   birthDay = Column(Date, nullable=true)


class Email(Base):
   __tablename__ = 'Email'
   id = Column(Integer, primary_key = True)
   sender_id = Column(Integer, ForeignKey(User.id))
   content = Column(String)
   created_date = Column(DateTime, default=datetime.datetime.utcnow)

   
class History(Base):
   __tablename__ = 'History'
   id = Column(Integer, primary_key = True)
   email_id = Column(Integer, ForeignKey(Email.id))
   receiver_id = Column(Integer, ForeignKey(User.id))
   status = Column(Integer,default=0)
   send_date = Column(DateTime, default=datetime.datetime.utcnow)
   # status(0: chưa đọc; 1: dã đọc; 2: đã xóa)

class Trash(Base):
   __tablename__ = 'Trash'
   id = Column(Integer, primary_key = True)
   sender_id = Column(Integer, ForeignKey(User.id))
   content = Column(String)
   deleted_date = Column(DateTime, default=datetime.datetime.utcnow)   

# Compile Create
Base.metadata.create_all(engine)

# baseModel
class signUp_Info(BaseModel):
    userName: str
    password: str
    password2: str

class signIn_Info(BaseModel):
    userName: str
    password: str

class Email_Info(BaseModel):
    userName: str
    content: str

class Receiver_Info(BaseModel):
    email_id: int
    receiver_name: str

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# Method

SECRET_KEY = "051562e151321231dsad2136123f6848b1561a5132a3013ca32135ab56156d16"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hashPassword(password):
    return pwd_context.hash(password)

def verifyPassword(passwordInput, passwordDatabase):
    return pwd_context.verify(passwordInput, passwordDatabase)

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post('/signUp/',response_model= bool)
async def signUp(r: signUp_Info = Depends()):
    if r.password != r.password2:
        return False
         
    query = select([User.id]).where(User.userName == r.userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        return False

    stmt=insert(User).values(userName = r.userName ,password =hashPassword(r.password))
    con = engine.connect()
    con.execute(stmt)
    return True

@app.post('/signIn/',response_model= bool)
async def signIn(r: signIn_Info = Depends()):
    query = select([User.id]).where(User.userName == r.userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        query = select([User]).where(and_(User.userName == r.userName))
        result = await database.fetch_one(query)    
        if verifyPassword(r.password,result['password']): 
            return True
        return False
    return False

@app.post('/email/createMail/',response_model= int)
async def createMail(r: Email_Info = Depends()):
    query = select([User.id]).where(User.userName == r.userName)
    id_user_ = await database.fetch_one(query)

    if id_user_:
        stmt = insert(Email).values(sender_id = id_user_["id"] ,content = r.content).returning(Email.id)
        con = engine.connect()
        result = con.execute(stmt)
        for row in result:
            return row['id']
            
    return -1


@app.post('/email/addReceiver/',response_model= bool)
async def createMail(r: Receiver_Info = Depends()):

    query = select([User.id]).where(User.userName == r.receiver_name)
    id_recei_ = await database.fetch_one(query)

    if id_recei_:
        stmt = insert(History).values(email_id = r.email_id ,receiver_id = id_recei_["id"])
        con = engine.connect()
        con.execute(stmt)
        return True
    return False

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

@app.get('/mail/getSentMail/')
async def getSentMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_recei_ = await database.fetch_one(query)

    if id_recei_:
        stmt = select([Email,User]).where(and_(Email.sender_id == id_recei_['id'],Email.sender_id == User.id))
        result = con.execute(stmt)
        listMail = list()
        for i in result:
            listMail.append(i)
        return listMail
    return null

@app.get('/mail/getDeletedMail/')
async def getDeletedMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_recei_ = await database.fetch_one(query)

    if id_recei_:
        # stmt = (select([History]).where(History.status == 2))
        # res = con.execute(stmt)
        
        # arrId = list()
        # for i in res:
        #     if not(i['email_id'] in arrId):
        #         arrId.append(i['email_id'])  

        # listMail = set()
        
        # stmt = select([Email]).where(Email.id.in_(arrId))
        # result = con.execute(stmt)
        

        # for i in result:
        #     listMail.append(i)
        listMail = set()
        stmt = select([Trash,User]).where(and_(Trash.sender_id == id_recei_['id'], Trash.sender_id == User.id))
        result = con.execute(stmt)
        for i in result:
            listMail.add(i)
        
        return listMail
    return null

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
                stmt = (update(History).where(and_(History.email_id == mail_del)).values(status = 1))
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

@app.get('/mail/getAll/')
async def AllMal():
    con = engine.connect()
    stmt = (select([Email]))
    result = con.execute(stmt)

    listMail = list()
    for i in result:
        listMail.append(i)
    return listMail

@app.get('/mail/getNormalMail/')
async def normalMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)
    if id_user_:
        stmt = (select([Email])).where(Email.sender_id == id_user_['id'])
        result = con.execute(stmt)
        
        arrId = set()
        for i in result:
            if not(i['id'] in arrId):
                arrId.add(i['id'])  
        
        stmt = (select([History])).where(History.receiver_id == id_user_['id'])
        result = con.execute(stmt)
        for i in result:
            if not(i['receiver_id'] in arrId):
                arrId.add(i['receiver_id']) 
        
        stmt = select([Email,User]).where(and_(Email.id.in_(arrId),Email.sender_id == User.id))
        result = con.execute(stmt)
        listMail = list()
        for i in result:
            listMail.append(i)

        return listMail
    return False


@app.get('/mail/getReceiveMail/')
async def receiveMail(userName: str):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)
    if id_user_:
        arrId = list()
        
        stmt = (select([History])).where(History.receiver_id == id_user_['id'])
        result = con.execute(stmt)
        for i in result:
            if not(i['email_id'] in arrId):
                arrId.append(i['email_id']) 
        
        stmt = select([Email,User]).where(and_(Email.id.in_(arrId),Email.sender_id == User.id))
        result = con.execute(stmt)      
        listMail = list()
        for i in result:
            listMail.append(i)

        return listMail
    return False

@app.post('/user/UserInfo/')
async def updateInfo(userName: str,
                        new_fullName: str,
                        new_birthDay: datetime.date
                        ):
    con = engine.connect()
    query = select([User.id]).where(User.userName == userName)
    id_user_ = await database.fetch_one(query)
    if id_user_:
        stmt = update(User).where(User.id == id_user_['id']).values(fullName = new_fullName, birthDay = new_birthDay)
        result = con.execute(stmt)
        return True
    return False

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=3001, reload=True)
