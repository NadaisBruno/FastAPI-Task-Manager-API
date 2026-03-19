from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from database import Base
from datetime import datetime


# Esta classe representa a tabela "tasks" na base de dados.
# Ao herdar de Base(declarative_base), o sqlalchemy sabe que esta classe deve ser mapeada para uma tabela real
# __tablename__ define o nome da tabela no banco de dados
class Task(Base):
    __tablename__ = "tasks"

    # 'id' identifica o tipo de tarefa
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    # identifica se a tarefa esta concluida e por defeito comeca por False
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # com o 'user_id' sabemos a quem pertence a tarefa
    # foreignkey liga esta tarefa ao utilizador na tabela 'users' em models\user.py
    user_id = Column(Integer, ForeignKey("users.id"))
