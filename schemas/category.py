from pydantic import BaseModel, ConfigDict


# schema usado para criar uma categoria na API
class CriarCategory(BaseModel):
    # nome da categoria
    name: str


class RespostaCategory(BaseModel):
    # identificador unico da categoria
    id: int
    # nome da categoria
    name: str
    # saber a quem pertence a categoria
    user_id: int

    # permite que o Pydantic converta objetos SqlAlchemy em JSON automaticamente
    model_config = ConfigDict(from_attributes=True)


# schema usdo para devolver uma lista paginada de categorias que inclui informacoes de paginacao e a lista de categorias
# 'categorias' contem a lista de categorias da página atual e cada elemento segue a estrutura definida no schema RespostaCategory
class ListaCategories(BaseModel):
    total: int
    page: int
    limit: int
    categorias: list[RespostaCategory]
