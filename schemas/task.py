from pydantic import BaseModel, ConfigDict
from typing import Optional, List  # Optional serve para declarar os campos opcionais
from datetime import datetime


# schema usado para criar uma tarefa na API
# apenas inclui title e description porque os restantes campos(id, completed, created_at, user_id) sao definidos pelo backend
class CriarTask(BaseModel):
    title: str
    description: str


# schema que devolve os dados da db
class RespostaTask(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    # permite que o Pydantic converta objetos SqlAlchemy em JSON automaticamente
    model_config = ConfigDict(from_attributes=True)


# schema que serve para actualizar uma tarefa(task) existente
# todos os campos sao opcionais porque no endpoint PATCH,em router\tasks.py, o cliente pode enviar apenas os campos
# que deseja alterar e por isso usamos 'Optional'
class ActualizarTask(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]


# schema usdo para devolver uma lista paginada de tarefas que inclui informacoes de paginacao e a lista de tarefas
# 'tasks' contem a lista de tarefas da página atual e cada elemento segue a estrutura definida no schema RespostaTask
class ListaTasks(BaseModel):
    total: int
    page: int
    limit: int
    tasks: List[RespostaTask]

