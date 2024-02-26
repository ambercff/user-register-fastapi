from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from databases import Database
from sqlalchemy.pool import NullPool
from models import Base

DATABASE_URL = "sqlite:///./data.db"

# Gerenciar conexão com banco de dados
db = Database(DATABASE_URL)

# Estabelecendo e gerenciando a conexão com o banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=NullPool)

# Armazenando informações sobre as tabelas
metadata = MetaData()

# Criando todas as tabelas e usamos o bind para especificar que as tabelas devem ser criadas utilizando a conexão do 'engine'
Base.metadata.create_all(bind = engine)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()