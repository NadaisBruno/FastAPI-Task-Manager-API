from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # categoria fica associada ao utilizador e por isso usamos 'users.id'
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
