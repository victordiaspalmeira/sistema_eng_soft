import flask
import sqlite3
from sqlite3_manager import (
    create_connection, get_user, create_user, create_inst, create_curs, 
    update_user, update_inst, update_curs, get_user, get_inst, get_curs
)

from werkzeug.security import check_password_hash, generate_password_hash

from flask import (
    request
)
from flask_cors import (
    CORS, cross_origin
)

app = flask.Flask(__name__)
CORS(app, support_credentials=True)
app.config["DEBUG"] = True


@app.route('/login', methods=('GET','POST'))
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Insira o nome de usuário.'
        elif not password:
            error = 'insira uma senha.'

        if error is None:
            conn = create_connection('engsoft.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            command = f"SELECT * FROM USER WHERE username = '{username}'"
            c.execute(command)
            user = get_user(username)

            if user is None:
                error = 'Nome de usuário não encontrado.'
            elif not check_password_hash(user['password'], password):
                error = 'Senha incorreta.'

        if error is None:
            #Dicionário
            return {'id': user['id'], 'cargo': user['cargo']}
        else:
            return {'message': error}, 403
    else:
        return 'BAD LOGIN', 403

@app.route('/user', methods=('PUT', 'GET','POST'))
@cross_origin(supports_credentials=True)
def user():
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == 'PUT': #Cadastro
        user_dict = {
            'inst_id': request.form['inst_id'],
            'username': request.form['username'],
            'password': request.form['password'],
            'nome': request.form['nome'],
            'sobrenome': request.form['sobrenome'],
            'telefone': request.form['telefone'],
            'email': request.form['email'],
            'cargo': request.form['cargo']
        }

        error = None

        try:
            c.execute(f"SELECT * FROM USER WHERE username = '{user_dict['username']}'")
            res = c.fetchall()
            if (len(res)>0):
                error = 'Nome de usuário não disponível..'
        except Exception as e:
            print(e)
            pass

        if error is None:
            try:
                create_user(user_dict)
                return {'message': 'Usuário registrado com sucesso!'}, 200
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    elif request.method == 'GET': #Visualização
        try:
            username = request.form['username']
            id = None
        except:
            username = None
            try:
                id = request.form['id']
            except:
                return {'message': 'Insira uma chave para busca de usuário.'}, 403
        user_data = get_user(username, id)
        return dict(zip(user_data.keys(), user_data)), 200

    elif request.method == 'POST': #Atualização
        user_dict = {
            'id': request.form['id'],
            'inst_id': request.form['inst_id'],
            'nome': request.form['nome'],
            'sobrenome': request.form['sobrenome'],
            'telefone': request.form['telefone'],
            'email': request.form['email'],
            'cargo': request.form['cargo']
        }

        error = None    

        try:
            c.execute(f"SELECT * FROM USER WHERE id = '{user_dict['id']}'")
            res = c.fetchall()
            print(len(res))
            if not (len(res)>0):
                error = 'Usuário não encontrado..'
        except Exception as e:
            print('UPDATE USER ERROR', e)
            pass

        if error is None:
            try:
                update_user(user_dict)
                return 'Usuário atualizado com sucesso!'
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    else:
        return {'message': 'NOT FOUND'}, 404

@app.route('/inst', methods=('PUT', 'GET', 'POST'))
@cross_origin(supports_credentials=True)
def inst():
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if request.method == 'PUT':
        inst_dict = {
            'inst_type': request.form['inst_type'],
            'visivel': request.form['visivel'],
            'nome': request.form['nome'],
            'endereco': request.form['endereco'],
            'cidade': request.form['cidade'],
            'estado': request.form['estado'],
            'credenciamento': request.form['credenciamento'],
            'mantenedora': request.form['mantenedora'],
        }

        error = None

        try:
            c.execute(f"SELECT * FROM INST WHERE nome = '{inst_dict['nome']}'")
            res = c.fetchall()
            if (len(res)>0):
                error = 'instituição já cadastrada.'
        except Exception as e:
            print(e)
            pass

        if error is None:
            try:
                create_inst(inst_dict)
                return {'message': 'REGISTERED'}, 200
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    elif request.method == 'GET':
        try:
            nome = request.form['nome']
            id = None
        except:
            nome = None
            try:
                id = request.form['id']
            except:
                return {'message': 'Insira uma chave para busca de instituição.'}, 403
        inst_data = get_inst(nome, id)
        return dict(zip(inst_data.keys(), inst_data)), 200    

    elif request.method == 'POST':
        inst_dict = {
            'id': request.form['id'],
            'inst_type': request.form['inst_type'],
            'visivel': request.form['visivel'],
            'nome': request.form['nome'],
            'endereco': request.form['endereco'],
            'cidade': request.form['cidade'],
            'estado': request.form['estado'],
            'credenciamento': request.form['credenciamento'],
            'mantenedora': request.form['mantenedora']
        }
        
        error = None    

        try:
            c.execute(f"SELECT * FROM INST WHERE id = '{inst_dict['id']}'")
            res = c.fetchall()
    
            if not (len(res)>0):
                error = 'Instituição não encontrada.'
        except Exception as e:
            print('UPDATE INST ERROR', e)
            pass

        if error is None:
            try:
                update_inst(inst_dict)
                return {'message': 'Instituição atualizada.'}, 200 
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403    

@app.route('/curs', methods=('PUT', 'GET', 'POST'))
@cross_origin(supports_credentials=True)
def curs():
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == 'PUT': #Cadastro
        curs_dict = {
            'inst_id': request.form['inst_id'],
            'nome': request.form['nome'],
            'grau': request.form['grau'],
            'codigo_emec': request.form['codigo_emec'],
            'ato_auto': request.form['ato_auto'],
            'ato_reco': request.form['ato_reco'],
            'ato_reno': request.form['ato_reno'],
            'renov': request.form['renov'],
            'obs': request.form['obs']
        }

        error = None

        try:
            c.execute(f"SELECT * FROM CURS WHERE nome = '{curs_dict['nome']}' and inst_id = '{curs_dict['inst_id']}'")
            res = c.fetchall()
            print(len(res))
            if (len(res)>0):
                error = 'Curso já registrado na instituição.'
        except Exception as e:
            print('CURS', e)
            pass

        if error is None:
            try:
                create_curs(curs_dict)
                return {'message': 'Cadastrado com sucesso!'}, 200
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    elif request.method == 'GET':
        try:
            nome = request.form['nome']
            inst_id = request.form['inst_id']
        except:
            return {'message': 'Insira uma chave para busca de curso.'}, 403
        curs_data = get_curs(nome, inst)
        return dict(zip(curs_data.keys(), curs_data)), 200

    elif request.method == 'POST':
        curs_dict = {
            'id': request.form['id'],
            'nome': request.form['nome'],
            'grau': request.form['grau'],
            'codigo_emec': request.form['codigo_emec'],
            'ato_auto': request.form['ato_auto'],
            'ato_reco': request.form['ato_reco'],
            'ato_reno': request.form['ato_reno'],
            'renov': request.form['renov'],
            'obs': request.form['obs']
        }
        error = None    

        try:
            res = get_curs(curs_dict['nome'], curs_dict['id'])
    
            if not (len(res)>0):
                error = 'Curso não encontrado.'
        except Exception as e:
            print('UPDATE CURS ERROR', e)
            pass

        if error is None:
            try:
                update_curs(curs_dict)
                return {'message': 'Curso atualizado com sucesso.'}, 200
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    else:
        return {'message': 'NOT FOUND'}, 404.

if __name__ == "__main__":
    app.run(debug=True)