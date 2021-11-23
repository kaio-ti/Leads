from datetime import datetime, timedelta
from app.configs.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import ( NULLTYPE, TIMESTAMP, String, DateTime)
from dataclasses import dataclass

from app.exceptions.exceptions import InvalidCPFError, InvalidKeysError, InvalidNotUniqueCpfError, InvalidTypeError


@dataclass
class Vacinacao(db.Model):

    allowed_keys = ['cpf', 'name', 'vaccine_name', 'health_unit_name']

    cpf: str
    name: str
    first_shot_date: int
    second_shot_date: int
    vaccine_name:str
    health_unit_name:str

    first_shot = datetime.now()
    second_shot = timedelta(days=90)

    __tablename__ = "vaccine_cards"

    cpf = Column(String, primary_key=True)

    name = Column(String, nullable=False)
    first_shot_date = Column(db.DateTime, default=datetime.utcnow)
    second_shot_date = Column(db.DateTime, default=first_shot + second_shot)
    vaccine_name = Column(String, nullable=False )
    health_unit_name = Column(String)

    @staticmethod
    def validation(data):


        for inputs in Vacinacao.allowed_keys:
            if inputs not in data.keys():
                raise InvalidKeysError  

        for inputs in data.values():
            if type(inputs) is not str:
                raise InvalidTypeError

        if len(data['cpf']) != 11:
            raise InvalidCPFError

        cpf =  (Vacinacao.query.filter(Vacinacao.cpf==data['cpf']).one_or_none())

        if cpf is not None:
            raise InvalidNotUniqueCpfError
        