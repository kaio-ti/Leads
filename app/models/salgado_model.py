from sqlalchemy import Column, Integer, String, Float
from app.configs.database import db


class SalgadoModel(db.Model):

    __tablename__ = "salgados"

    id = Column(Integer, primary_key=True)
    nome = Column(String(60), nullable=False, unique=True)
    preco = Column(Float, nullable=False)
