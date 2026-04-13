from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from schemas.task import CriarTask
from models.user import User
from models.task import Task
from security import buscar_utilizador_autenticado
from schemas.task import ActualizarTask
from schemas.task import RespostaTask
from schemas.task import ListaTasks

# criamos um router para agrupar os endpoints
router = APIRouter()


@router.post("/tasks", response_model=RespostaTask)  # usamos response model para definir o formato de respostas da API garantindo que apenas os campos definidos em Resposta Task sao devolvidos
def criar_tasks(
        # contem os dados enviados pelo cliente(title e description)
        task: CriarTask,
        # utilizador autenticado obtido a partir do token
        utilizador: User = Depends(buscar_utilizador_autenticado),
        # ligacao a base de dados
        db: Session = Depends(get_db)):
    nova_task = Task(
        # titulo da tarefa enviado pelo cliente
        title=task.title,
        # descricao da tarefa enviada pelo cliente
        description=task.description,
        # associamos a tarefa a respetiva categoria
        category_id=task.category_id,
        # associamos a tarefa ao utilizador autenticado e usamos 'utilizador.id' para garantir que a tarefa pertence a quem fez o pedido
        user_id=utilizador.id
    )
    # adicionamos o objeto nova_task a sessao da base de dados
    # isto diz ao SQLAlchemy que queremos guardar esta tarefa
    db.add(nova_task)

    # gravar definitavamente na base de dados
    db.commit()

    # actualiza o objeto nova_task com os dados gerados pela base de dados, por exemplo, ‘id’ e 'created_at'
    db.refresh(nova_task)

    task_db = db.query(Task).options(joinedload(Task.category)).filter(Task.id == nova_task.id).first()

    print(task_db.category)
    # devolvemos a tarefa criada
    # o FastAPI vai converter o objeto Task em JSON automaticamente
    return task_db


# endpoint que permite irmos buscar a lista paginada de tarefas associadas ao utilizador autenticado
@router.get("/tasks", response_model=ListaTasks)
def listar_tasks(
        # page indica qual a pagina de resultados que queremos obter
        page: int = 1,
        # quantas tarefas queremos que sejam mostradas por página
        limit: int = 10,
        # utilizador autenticado obtido a partir do token
        utilizador: User = Depends(buscar_utilizador_autenticado),
        # ligacao a base de dados
        db: Session = Depends(get_db)):

    # permite mostrar apenas a pagina pedida pelo utilizar/ignora tarefas de paginas anteriores
    offset = (page - 1) * limit

    # buscamos todas as tarefas que pertencem ao utilizador autenticado
    # db.query(Task) -> inicia uma consulta a tabela tasks
    # filter(Task.user_id == utilizador.id) -> filtra apenas as tarefas do utilizador com esse ‘id’
    # usamos joinedload para garantir que a category é carregada com a task
    query = db.query(Task).options(joinedload(Task.category)).filter(Task.user_id == utilizador.id)

    # aqui fazemos a contagem de quantas tarefas existem no total usando o count()
    # permite saber quantas páginas existem
    contagem_tasks = query.count()

    # ordenamos as tarefas pela data de criacao na ordem descendente
    query = query.order_by(Task.created_at.desc())

    # aplicamos paginacao a query
    # .offset(offset) -> ignora as tarefas das paginas anteriores
    # .limit(limit) -> devolve apenas um numero especifico de tarefas neste caso 10
    # all() executa a consulta e devolve as tarefas encontradas
    tasks = query.offset(offset).limit(limit).all()


    # devolvemos a paginacao e as tarefas em formato JSON
    return {
        "total": contagem_tasks,
        "page": page,
        "limit": limit,
        "tasks": tasks
    }


# endpoint que serve para irmos buscar uma task especifica atraves do ‘id’
@router.get("/tasks/{task_id}", response_model=RespostaTask)
def listar_task(
        # é o ‘id’ da tarefa que vem da url(por exemplo, http://localhost:8000/tasks/3)
        task_id: int,
        # utilizador autenticado obtido a partir do token
        utilizador: User = Depends(buscar_utilizador_autenticado),
        # ligacao a base de dados
        db: Session = Depends(get_db)):
    # fazemos a consulta com o filtro para procurar o ‘id’ da task
    task = db.query(Task).filter(Task.id == task_id).first()
    # se a tarefa nao existir lancamos o erro 404 - not found
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa nao existe na base de dados")
    # verificamos se a tarefa pertence ao utilizador autenticado
    # se o user_id for diferente do ‘id’ do utilizador, lanço um erro
    # devolvemos erro 404 para nao revelar que a tarefa existe por motivos de segurança
    if task.user_id != utilizador.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task


# endpoint usado para actualizar a base de dados
@router.patch("/tasks/{task_id}", response_model=RespostaTask)
def update_task(
        task_id: int,
        # dados enviados pelo utilizador, localizado em schemas\task.py, para actualizar a tarefa
        task: ActualizarTask,
        # utilizador autenticado atraves do ‘token’
        utilizador: User = Depends(buscar_utilizador_autenticado),
        # ligacao a base de dados
        db: Session = Depends(get_db)):
    # fazemos a consulta com o ‘id’ da tarefa // procurar a task na base de dados
    task_db = db.query(Task).filter(Task.id == task_id).first()
    # verificar se a tarefa existe
    if not task_db:
        raise HTTPException(status_code=404, detail="Tarefa não existe")
    # verificamos se a tarefa pertence ao utilizador autenticado
    # se o user_id for diferente do ‘id’ do utilizador lanço um erro
    # devolvemos erro 404 para nao revelar que a tarefa existe por motivos de segurança
    if task_db.user_id != utilizador.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    # task ⇒ objeto criado a partir do JSON enviado pelo utilizador(schema class ActualizarTask, em models\task.py)
    # task_db -> objeto da tarefa que ja existe na base de dados
    # verificamos se o utilizador modificou o title da task
    if task.title is not None:
        # actualizamos o title da task da base de dados
        # copiamos o valor vindo do utilizador (task.title)
        # para o objeto da base de dados (task_db.title)
        task_db.title = task.title
    if task.description is not None:
        task_db.description = task.description
    if task.completed is not None:
        task_db.completed = task.completed

    # guardar alteracoes na base de dados
    db.commit()

    # sincroniza o task_db com a base de dados após o commit, garantindo que temos os valores mais recentes guardados
    db.refresh(task_db)

    # devolvemos a tarefa actualizada
    return task_db


# endpoint usado para eliminar tarefas
@router.delete("/tasks/{task_id}", response_model=RespostaTask)
def delete_task(
        task_id: int,
        utilizador: User = Depends(buscar_utilizador_autenticado),
        db: Session = Depends(get_db)):
    # procurar a task na base de dados
    # equivalente em SQL: SELECT * FROM tasks WHERE id = task.id
    task_db_delete = db.query(Task).filter(Task.id == task_id).first()
    if task_db_delete is None:
        raise HTTPException(status_code=404, detail="Tarefa não existe")
    # verificamos se a task pretence ao utilizador
    # se nao encontrar, devolvemos erro para impedir acesso a tarefas de outros utilizadores
    if task_db_delete.user_id != utilizador.id:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    # eliminamos a tarefa da base de dados
    db.delete(task_db_delete)

    # gravamos as alteracoes
    db.commit()

    # sincroniza a task_db_delete com a base de dados apos o commit
    # db.refresh(task_db_delete)

    # devolvemos a tarefa eliminada
    return task_db_delete
