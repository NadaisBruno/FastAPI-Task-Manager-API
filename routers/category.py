from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.category import RespostaCategory
from schemas.category import CriarCategory, ListaCategories
from models.user import User
from models.category import Category
from security import buscar_utilizador_autenticado

router = APIRouter()


# endpoint para criar as categorias
@router.post("/categories", response_model=RespostaCategory)
def criar_categories(
        #
        categoria: CriarCategory,
        # utilizador autenticado obtido a partir do token
        utilizador: User = Depends(buscar_utilizador_autenticado),
        # ligacao a base de dados
        db: Session = Depends(get_db)):
    # criamos uma nova categoria com os dados enviados pelo utilizador
    new_category = Category(
        name=categoria.name,
        user_id=utilizador.id
    )

    # adicionamos a nova categoria a sessao da db
    db.add(new_category)
    # gravamos na base de dados
    db.commit()
    # actualiza o objeto new_category com os dados gerados pela base de dados
    # isto diz ao SQLAlchemy que queremos guardar esta categoria
    db.refresh(new_category)
    # devolvemos a categoria criada em formato JSON
    return new_category


#
@router.get("/categories", response_model=ListaCategories)
def listar_categories(
        page: int = 1,
        limit: int = 10,
        utilizador: User = Depends(buscar_utilizador_autenticado),
        db: Session = Depends(get_db)):

    # permite mostrar apenas a pagina pedida pelo utilizar
    # (page - 1) -> ajusta a pagina para comecar do zero
    # limit ⇒ quantos registos por página
    offset = (page - 1) * limit

    # buscamos todas as categorias que pertencem ao utilizador autenticado
    query = db.query(Category).filter(Category.user_id == utilizador.id)

    # fazemos a contagem do total de categorias do utilizador
    contagem_categorias = query.count()

    # ordenamos as categorias pela data de criacao na ordem descendente
    # query = query.order_by(Category.created_at.desc())

    # aplicamos paginacao a query
    # .offset(offset) -> ignora as categorias das paginas anteriores
    # .limit(limit) -> devolve apenas um numero especifico de categorias neste caso 10
    #  all() executa a consulta e devolve as categorias encontradas
    categories = query.offset(offset).limit(limit).all()

    # devolvemos a paginacao e as categorias em foramto JSON
    return {
        "total": contagem_categorias,
        "page": page,
        "limit": limit,
        "categorias": categories
    }
