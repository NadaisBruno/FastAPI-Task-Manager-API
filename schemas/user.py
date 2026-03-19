# pydantic verifica se o email é valido, se os campos obrigatorios existem, se algo esta mal(pydantic valida os dados) - protege a API
# configdict permite que o pydantic consiga transformar um objeto sqalchemy numa resposta JSON automaticamente, sem isto ele so aceita dicionarios
from pydantic import BaseModel, EmailStr, ConfigDict


# Quando o cliente faz post /register ele diz a API que precisa:
# - email
# - password
class CriarUsuario(BaseModel):
    email: EmailStr
    password: str


# Quando o cliente faz post /login ele diz a API que precisa:
# - email
# - password
class LoginUsuario(BaseModel):
    email: EmailStr
    password: str


# Quando a API devolve dados do utilizador iclui:
# - id
# - email
# Não inclui passwor_hash, is_active e created_at porque nao podemos expor estas informações por seguranca
class RespostaUsuario(BaseModel):
    id: int
    email: EmailStr
    # Permite que o schema aceite objetos sqalchemy
    # sem isto o Pydantic so aceitaria dicionarios
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
