from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime


# Esta classe representa a tabela "users" na base de dados.
# Ao herdar de Base(declarative_base), o sqlalchemy sabe que esta classe deve ser mapeada para uma tabela real
# __tablename__ define o nome da tabela no banco de dados
class User(Base):
    __tablename__ = "users"

    # Criamos a coluna 'id' como inteiro(Integer)
    # primary key=true significa que esta coluna identifica unicamente cada registo na tabela(nao pode ser repetido)
    id = Column(Integer, primary_key=True)
    # 'unique' garante que nao repete o mesmo email, ou seja, é unico
    # equivalente no sqlite: 'email text unique not null'
    email = Column(String, unique=True, index=True, nullable=False)
    # guarda a password ja encriptada(hash)
    password_hash = Column(String, nullable=False)
    # Identifica se o utilizador está ativo
    # default=true significa que é criado ativo por defeito
    is_active = Column(Boolean, default=True)
    # passamos a funcao sem () para ser executada no momento de inserção
    created_at = Column(DateTime, default=datetime.utcnow)
