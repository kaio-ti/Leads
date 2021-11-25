from flask import request, current_app, jsonify
from app.exceptions.exceptions import InvalidKeysError, InvalidPhoneError, InvalidTypeError, NotUniqueEmailError, NotUniquePhoneError
from app.models.lead_model import Leads


def create_lead():
    try:
        data = request.json
        Leads.validation(data)
        lead = Leads(**data)
        current_app.db.session.add(lead)
        current_app.db.session.commit()

        return jsonify(lead), 201

    except InvalidTypeError:
        return {"message": "Dados precisam ser strings"}, 400
    except InvalidKeysError:
        return {"message": "Corpo da requisição com informações desnecessárias"}, 400
    except NotUniqueEmailError:
        return {"message": "Email já presente no banco de dados"}, 409
    except NotUniquePhoneError:
        return {"message": "Número já presente no banco de dados"}, 409
    except InvalidPhoneError:
        return {"message": "Número inválido, reveja seus dados"}, 400
 

def get_leads():
    response =  Leads.query.order_by(Leads.visits.desc()).all()
    if len(response) == 0:
        return {"message": "Erro, nenhum dado encontrado"}, 404
    return jsonify(response), 200

def update_leads():
    data = request.json

    if list(data.keys()) != ['email'] or type(data['email']) is not str:
        return {"message": "Dados da requisição inválidos"}, 404

    Leads.update_visit(data)

    return "", 204

def delete_leads():
    data = request.json

    if list(data.keys()) != ['email'] or type(data['email']) is not str:
        return {"message": "Dados da requisição inválidos"}, 404

    Leads.leads_deletion(data)

    return "", 204