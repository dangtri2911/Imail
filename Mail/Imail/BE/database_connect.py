import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

DATABASE_URL = "postgresql://postgres:tri29112001@localhost/demo"

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

Base = declarative_base()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

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

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Base.metadata.create_all(engine)

SECRET_KEY = "051562e151321231dsad2136123f6848b1561a5132a3013ca32135ab56156d16"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hashPassword(password):
    return pwd_context.hash(password)

def verifyPassword(passwordInput, passwordDatabase):
    return pwd_context.verify(passwordInput, passwordDatabase)

