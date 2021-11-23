from flask import request, current_app, jsonify
from app.exceptions.exceptions import InvalidCPFError, InvalidKeysError, InvalidNotUniqueCpfError, InvalidTypeError
from app.models.vacinacao_model import Vacinacao


def register_card():
    data = request.json

    try:
        Vacinacao.validation(data)
        formatted_data = {keys: value.upper() for keys,value in data.items()}
        for i in list(formatted_data.keys()):
            if i not in Vacinacao.allowed_keys:
                del formatted_data[i]
        vacina = Vacinacao(**formatted_data)
        current_app.db.session.add(vacina)
        current_app.db.session.commit()

        return {
            "cpf": vacina.cpf,
            "name": vacina.name,
            "first_shot_date": vacina.first_shot_date,
            "second_shot_date": vacina.second_shot_date,
            "vaccine_name": vacina.vaccine_name,
            "health_unit_name": vacina.health_unit_name
        }, 201

    except InvalidCPFError:
        return {"message": "CPF inválido, 11 dígitos numéricos necessários"},400
    except InvalidTypeError:
        return {"message": "Corpo da requisição inválido, necessário ser do tipo string"},400
    except InvalidKeysError:
        return {"message": "Campos inválidos"}, 400
    except InvalidNotUniqueCpfError:
        return {"message": "CPF já constante no banco de dados"},409

def get_vaccines():
    return jsonify(Vacinacao.query.all()), 200