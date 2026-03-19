from fastapi import APIRouter, HTTPException, Depends  # API routers cria um mini-grupo de endpoints(em vez de colocá-los todos no main.py)
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import CriarUsuario, LoginUsuario, RespostaUsuario, TokenResponse
from models.user import User
from security import hash_password
from security import verificar_password
from security import criar_token_accesso
from security import buscar_utilizador_autenticado

# criamos um router para agrupar endpoints relacionados com autenticação
router = APIRouter()


# response_model define o formato da resposta da API.
# Mesmo que o objeto ‘User’ tenha mais campos(password_hash, created_at, is_active)
# apenas os campos definidos em RespostaUsuario(localizado em schemas\user) serao enviados
# ao cliente - neste caso so envia, por motivos de seguranca, o ‘id’ e o email
@router.post("/register", response_model=RespostaUsuario)
# Session = Depends(get_db)= o fastapi cria uma sessao para esta request e entrega aqui
def register(user: CriarUsuario, db: Session = Depends(get_db)):
    # db ⇒ é a sessao ativa do SQLALQUEMY que permite comunicar com a base de dados
    # query(User) ⇒ inicia a consulta a tabela "users" representada pela classe User(localizada em models/user.py) // equivalente no sqlite SELECT * FROM users
    # filter ⇒ User.email representa a coluna da tabela
    #          user.email representa o email enviado pelo utilizador
    #            (equivalente em sqlite3 a WHERE email=?)
    # first() ->  executa a query e devolve:
    #           - um objeto User se encontrar o registo
    #           - None se nao existir nenhum utilizador com esse email
    #               (Equivalente a LIMIT 1 + fetchone() em sqlite3)
    utilizador_existente = db.query(User).filter(User.email == user.email).first()

    # verificamos na bd se o email ja existe no servidor(nao pode haver emails repetidos)
    if utilizador_existente is not None:
        raise HTTPException(status_code=409, detail="Este email já se encontra registado")

    # transformamos a password em hash seguro
    password_hash = hash_password(user.password)

    # criamos o objeto user(criamos um novo utilizador)
    novo_utilizador = User(email=user.email, password_hash=password_hash)
    # adicionamos o utilizador a sessao
    db.add(novo_utilizador)
    # gravamos na base de dados
    db.commit()
    # sincroniza o utilizador com a base de dados após o commit, ou seja, atualiza o utilizador com o ‘id’ gerado na base de dados
    db.refresh(novo_utilizador)
    return novo_utilizador


@router.post("/login", response_model=TokenResponse)
def login(user: LoginUsuario, db: Session = Depends(get_db)):
    utilizador_existente = db.query(User).filter(User.email == user.email).first()
    # se o utilizador nao existir levantamos uma excecao
    if utilizador_existente is None:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    # se a password que o utilizador escreveu nao corresponde a que esta guardada entao mostro erro
    if not verificar_password(user.password, utilizador_existente.password_hash):
        raise HTTPException(status_code=401, detail="Email ou password inválidos")

    #
    access_token = criar_token_accesso({"sub": utilizador_existente.email})

    return {"access_token": access_token,
            "token_type": "bearer"
            }


# endpoint protegido que devolve os dados do utilizador autenticado
# Antes de executar a funcao, o fastapi executa a dependencia 'buscar_utilizador_autenticado' que:
#  - recebe o token enviado no Header Authorization
#  - valida o JWT
#  - procura o utilizador na base de dados
#  - devolve o objeto User correpondente
@router.get("/me")
def me(utilizador: User = Depends(buscar_utilizador_autenticado)):
    return {
        "id": utilizador.id,
        "email": utilizador.email
    }
