from datetime import datetime
from app.configs.database import db
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import (TIMESTAMP, Integer, String)
from dataclasses import dataclass
import re
from flask import current_app

from app.exceptions.exceptions import InvalidKeysError, InvalidPhoneError, InvalidTypeError, NotUniqueEmailError 


@dataclass
class Leads(db.Model):

    allowed_keys = ['name', 'email', 'phone']
    
    id: int
    name: str
    email: str
    phone: str
    visits:int
    creation_date: str
    last_visit: str

    __tablename__ = "lead_cards"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    creation_date = Column(db.DateTime, nullable=True, default=datetime.utcnow())
    last_visit = Column(db.DateTime, nullable=True, default=datetime.utcnow())
    visits = Column(Integer, nullable=True, default=1)

    @staticmethod
    def validation(data):
        pattern = re.compile(r'^\([0-9]{2}\)[0-9]{5}\-[0-9]{4}$')
       
        for key in data.keys():
            if key not in Leads.allowed_keys:
                raise InvalidKeysError

        for value in data.values():
            if type(value) is not str:
                raise InvalidTypeError

        email = (Leads.query.filter(Leads.email==data['email']).one_or_none())
        phone = (Leads.query.filter(Leads.phone==data['phone']).one_or_none())


        if email is not None:
            raise NotUniqueEmailError

        if phone is not None:
            raise InvalidPhoneError

        if pattern.fullmatch(data["phone"]) is None:
            raise InvalidPhoneError

    def update_visit(data):


        specific = Leads.query.filter(Leads.email==data['email']).first()
        
        if specific is None:
            return {"message": "Email não encontrado"}, 404
        
        data["visits"] = Leads.visits + 1
        data["last_visit"] = datetime.utcnow()

        for key, value in data.items():
            setattr(specific, key, value)

        current_app.db.session.add(specific)
        current_app.db.session.commit()

        return "", 204

    def leads_deletion(data):

        specific = Leads.query.filter(Leads.email==data['email']).first()

        if specific is None:
            return {"message": "Email não encontrado"}, 404
        
        current_app.db.session.delete(specific)
        current_app.db.session.commit()
        return "", 204