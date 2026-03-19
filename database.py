from sqlalchemy import create_engine  # serve para gerir a conecao entre o python e a base de dados
from sqlalchemy.orm import declarative_base, sessionmaker

# é o mesmo que fazer em sqlite isto:  "with sqlite3.connect("tasks.db") as con"
engine = create_engine("sqlite:///./tasks.db")

# aqui descrevemos como sera a tabela mas ainda nao existe fisicamente
Base = declarative_base()

#
Base.metadata.create_all(engine)

# De cada vez que chamar-mos o sessionlocal sera criada uma nova sessao ligada ao engine(base de dados)
# A sessão é o objeto que usamos para fazer operacoes tais como:
# - adicionar dados, consultar, atualizar e fazer commit
SessionLocal = sessionmaker(bind=engine)


# aqui abrimos a coneção, usamos e depois fecha automaticamente - é equivalente no sqlite a isto:
# with sqlite3.connect("tasks.db") as con:
#    cursor = con.cursor()
#    cursor.execute(...)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()