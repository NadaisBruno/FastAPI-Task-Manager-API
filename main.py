from fastapi import FastAPI
from database import engine, Base
from routers import auth
from routers import tasks
from models import user

app = FastAPI()

# include_router liga os endpoints definidos no ficheiro routers/auth.py à aplicação principal
# Sem isto o FastAPI nao reconhece os endpoints criados com APIRouter()
# Ou seja, o /register e /login não apareceriam no Swagger nem existiriam na API
app.include_router(auth.router)

# include_router liga os endpoints definidos no ficheiro routers/tasks.py à aplicação principal
# Sem isto o FastAPI nao reconhece os endpoints criados com APIRouter()
app.include_router(tasks.router)

# Criamos na base de dados todas as tabelas definidas nas classes que herdam de Base(ex: user)
# Base é a classe base criada com "Base = declarative_base()" em database.py
# Base guarda uma lista de todas as classes que herdaram dela, neste caso, "class User(Base)" em user.py
# metadata é onde o sqlalchemy guarda:
# - lista de tabelas
# - estrutura das colunas
# - relacoes
# resumindo esta linha significa que vai à base de dados ligada pelo engine e cria todas as tabelas
# definidas nos models que ainda nao existem
Base.metadata.create_all(bind=engine)
