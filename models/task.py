from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
# liga tabela tasks á tabela categories
# permite usar task.category(objeto com o nome da categoria) em vez de so task.category_id(onde so aparece o id da categoria)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
# necessario para que o SQLAlchemy reconheca a class Category
# mesmo que nao seja usado diretamente é preciso para o relationship("Category") funcionar
from models.category import Category


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
    # com category_id ligamos tarefa ao id da categoria
    # foreignkey liga esta tarefa á categoria na tabela 'categories' em models\category.py
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    # associamos o nome da categoria à task // relationship permite trocar ‘IDs’, que sao so numeros, por objetos reais
    # lazy=joined ⇒ carrega automaticamente a categoria ao buscar tarefas
    category = relationship("Category", lazy="joined")
