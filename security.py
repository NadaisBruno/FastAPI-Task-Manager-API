from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
#import secrets
from jose import jwt, JWTError

#chave = secrets.token_hex(32)
#print(chave)


# ----------------CONSTANTES---------------------------
# IMPORTANTE: Constantes sao configurações fixas do sistema e nao devem ser alteradas durante execução
#    - ficam sempre no topo
#    - agrupadas
#    - são configurações globais
#    - não é para mexer no meio da lógica
#    - não é para redefinir dentro de funções
# Chave secreta usada para assinar ‘tokens’ e deve estar sempre numa variavel de ambiente, nao diretamente no codigo
# Gerada com secrets.token_hex(32) // Tenho de importar secrets para gerar um ‘token’, mas depois devo apagá-lo
SECRET_KEY = "a8c2a6d0cc984ef1184068ec7b053ab82021690eed9595cd2ec3198a3b44865d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Crio uma protecao automatica que obriga o utilizador a enviar um ‘token’
# valido antes de entrar num endpoint protegido.
# Se nao enviar o sistema bloqueia automaticamente
security = HTTPBearer(auto_error=True)

# usamos o algoritmo bcrypt que gera um salt garantindo hashes diferentes mesmo para passwords iguais
# deprecated=auto prepara futuras actualizacoes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# recebe a password em texto e transforma em hash seguro para armazenamento
def hash_password(password):
    return pwd_context.hash(password)


# aqui verificamos se a password corresponde a hash guardada usando 'verify' e devolve true ou false
def verificar_password(password, password_hash):
    return pwd_context.verify(password, password_hash)


def criar_token_accesso(data: dict):
    # Criamos uma cópia dos dados recebidos para evitar modificar o dicionário original por questoes de efeitos colaterais
    to_encode = data.copy()

    duracao_token = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Adicionamos ao payload(informação que vai dentro do ‘token’) o campo "exp"(expiration time)
    # Este campo é usado automaticamente na validação do JWT
    # Quando a data ultrapassar este valor, o ‘token’ torna-se invalido
    to_encode.update({"exp": duracao_token})

    # geramos e devolvemos o token JWT
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# A parte "credentials = Depends(security)" significa:
#  Antes de executar esta função, o FastAPI vai verificar
#  se o cliente enviou um ‘token’ no header "Authorization".
#  O cliente deve enviar algo assim:
#  Authorization: Bearer <token>
#  Se o header não existir ou estiver mal escrito,
#  o FastAPI devolve automaticamente erro 401
#  e a função nem chega a ser executada.
#  Se estiver correto, o FastAPI cria automaticamente
#  um objeto chamado "credentials" que contém:
#    credentials.scheme - normalmente "Bearer"
#    credentials.credentials - o ‘token’ real (JWT)
#  Ou seja, não precisamos verificar manualmente se começa
#  com "Bearer" nem dividir a ‘string’.
#  O FastAPI já faz essa isso por mim
#  Isto deixa o código mais simple e mais seguro
def buscar_utilizador_autenticado(
        # HTTPAuthorizationCredentials = estrutura que contem o token // Depends(security) = exige o token
        credentials: HTTPAuthorizationCredentials = Depends(security),

        # db é a sessão da base de dados usada para procurar o utilizador
        db: Session = Depends(get_db)
):
    # extraimos o JWT enviado pelo cliente no header Athorization: Bearer token
    token = credentials.credentials

    #  jwt.decode valida automaticamente:
    #    - a assinatura usando a SECRET_KEY
    #    - o algoritmo utilizado
    #    - a data de expiracao("exp")
    # Se tudo estiver correto devolve o conteudo interno do ‘token’, ou seja, o payload
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")

    # subject(sub) é o dono do token
    email = payload.get("sub")

    # verificar se o ‘token’ contem o campo "sub"(email do utilizador), se nao existir, o email é invalido
    if not email:
        raise HTTPException(status_code=401, detail="Token Inválido")

    # procuramos o utilizador na db
    utilizador_existente = db.query(User).filter(User.email == email).first()
    if utilizador_existente is None:
        raise HTTPException(status_code=401, detail="Utilizador inválido")

    return utilizador_existente

