from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session 
from database import * 
from models import *
from typing import List

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/user', response_model = UserRead)
async def create_user(item: UserCreate, db: Session = Depends(get_db)):
    
    db_item = UserDB(**item.model_dump()) # Convertendo o modelo pydantic para um dicionario
    db.add(db_item) # Adicionando o item a sessao do banco de dados
    db.commit() # Commitando as alterações do banco
    db.refresh(db_item)
    
    return db_item

@app.put('/user/{user_id}', response_model = UserRead)
async def update_item(user_id: int, upd_user: UserUpdate, db: Session = Depends(get_db)):
    
    # Busca no banco de dados o item cujo id seja o equivalente ao do banco e retorna o primeiro item encontrado
    db_item = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if not db_item:
        raise HTTPException(status_code = 404, detail = "Usuário não encontrado")
    
    # Utilizamos o for para percorrer todos os pares key-value do ItemUpdate
    # O model_dump converte o objeto para um dicionário
    
    for key, value in upd_user.model_dump().items():
        # Utilizamos o set attribute para definirmos o valor de um atributo dentro de um objeto, passando o objeto e o atributo que desejamos definir/modificar e o valor que deseja atribuir ao mesmo
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    
    return db_item

@app.delete('/user/{user_id}', response_model = UserRead)
async def get_item(user_id: int, db: Session = Depends(get_db)):
    
    db_item = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    if db_item:
        db.delete(db_item)
        db.commit()
       
    else:
        raise HTTPException(status_code = 404, detail = "Usuário não encontrado")
    
# @app.get('/get_user/{user_id}', response_model = UserRead)
# async def get_item(user_id: int, db: Session = Depends(get_db)):
    
#     db_item = db.query(UserDB).filter(UserDB.id == user_id).first()
    
#     if db_item is None:
#         raise HTTPException(status_code = 404, detail = "Usuário não encontrado")
    
#     return db_item

@app.get('/user', response_model = List[UserRead])
async def get_all_users(db: Session = Depends(get_db)):
    
    db_items = db.query(UserDB).all()
    
    return db_items