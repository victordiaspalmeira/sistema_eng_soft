import flask
import sqlite3
from sqlite3_manager import (
    create_connection, get_user, create_user, create_inst, create_curs, 
    update_user, update_inst, update_curs, get_user, get_all_users, get_inst, get_curs, get_all_curs, get_all_insts,
    get_user_cargo
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
@app.route('/header/', methods=('GET','POST'))
@app.route('/header/<user_id>', methods=('GET','POST'))
@cross_origin(supports_credentials=True)
def header_test(user_id=None):
    return 'USER_ID: '+ str(user_id), 200

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
        return {'message': 'NOT FOUND'}, 404

@app.route('/user/', methods=('PUT', 'GET','POST'))
@app.route('/user/<user_id>', methods=('PUT', 'GET','POST'))
@cross_origin(supports_credentials=True)
def user(user_id=None):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    _user_id = request.headers['authorization']
    aux = get_user(id=_user_id)
    cargo, inst_id = aux['cargo'], aux['inst_id']

    if request.method == 'PUT': #Cadastro
        if cargo.lower() not in ['diretor', 'superintendente', 'debug']:
            return {'message': 'Você não deveria estar aqui.'}, 403
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
                error = 'Nome de usuário não disponível.'
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
        if user_id is not None:              
            user_data = get_user(id=user_id)
            return dict(zip(user_data.keys(), user_data)), 200
        else:
            user_list = get_all_users(cargo, inst_id)
            user_data = dict()
            for user in user_list:
                u = dict(zip(user.keys(), user))
                user_data[u['id']] = u 
            return user_data, 200
        
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

@app.route('/inst/', methods=('PUT', 'GET', 'POST'))
@app.route('/inst/<inst_id>', methods=('PUT', 'GET', 'POST'))
@cross_origin(supports_credentials=True)
def inst(inst_id=None):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    _user_id = request.headers['authorization']
    aux = get_user(id=_user_id)
    cargo, _inst_id = aux['cargo'], aux['inst_id']
    if _user_id is None:
        return {'message': 'FORBIDDEN'}, 403
    if request.method == 'PUT':
        if cargo.lower() not in ['dirigente institucional', 'superintendente', 'debug']:
            return {'message': 'Você não deveria estar aqui.'}, 403
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
        if (inst_id is not None):
            inst_data = get_inst(id=inst_id)
            return dict(zip(inst_data.keys(), inst_data)), 200
        else:
            inst_list = get_all_insts(cargo)
            inst_data = dict()
            for inst in inst_list:
                try:
                    u = dict(zip(inst.keys(), inst))
                    inst_data[u['id']] = u
                except:
                    inst_data = None
            
            return inst_data



    elif request.method == 'POST':
        if cargo.lower() not in ['diretor', 'superintendente', 'debug']:
            return {'message': 'Você não deveria estar aqui.'}, 403
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
    _user_id = request.headers['authorization']
    cargo = get_user_cargo(_user_id)

    if request.method == 'PUT': #Cadastro
        if cargo.lower() not in ['diretor', 'superintendente', 'debug']:
            return {'message': 'Você não deveria estar aqui.'}, 403
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
        query_type = True
        try:
            nome = request.form['nome']
            inst_id = request.form['inst_id']
            if((nome is not None) or (inst_id is not None)):
                query_type = False
        except:
            try:
                inst_id = request.form['inst_id']
                if inst_id is not None:
                    query_type = True
            except:
                pass

        if query_type:
            curs_list = get_all_curs(inst_id)
            curs_data = dict()
            for curs in curs_list:
                u = dict(zip(curs.keys(), curs))
                curs_data[u['id']] = u
            return curs_data
        else:
            curs_data = get_curs(nome, inst_id)
        return dict(zip(curs_data.keys(), curs_data)), 200

    elif request.method == 'POST':
        if cargo.lower() not in ['diretor', 'superintendente', 'debug']:
            return {'message': 'Você não deveria estar aqui.'}, 403
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
            error = 'Curso não encontrado.'
            pass

        if error is None:
            try:
                update_curs(curs_dict)
                return {'message': 'Curso atualizado com sucesso.'}, 200
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    else:
        return {'message': 'NOT FOUND'}, 404

if __name__ == "__main__":
    app.run(debug=True)