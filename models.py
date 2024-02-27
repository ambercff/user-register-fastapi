from pydantic import BaseModel, validator
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Modelo pydantic para criar usuario
class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    email: str
    
# Modelo pydantic para retornar usuarios
class UserRead(BaseModel):
    id: int
    name: str
    username: str
    password: str
    email: str
    
# Modelo pydantic para atualizar usuario
class UserUpdate(BaseModel):
    name: str
    username: str
    password: str 
    email: str  
    
# Modelo pydantic que contém todos os campos
class User(UserCreate, UserUpdate):
    pass


# Modelo SQLAlchemy para criar as tabelas no banco
class UserDB(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True)
    username = Column(String, index = True)
    password = Column(String, index = True)
    email = Column(String, index = True)