import flask
import sqlite3
from sqlite3_manager import (
    create_connection, get_user, create_user, create_inst, create_curs, 
    update_user, update_inst, update_curs, get_user
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
            error = 'USERNAME MISSING'
        elif not password:
            error = 'PASSWORD MISSING'

        if error is None:
            conn = create_connection('engsoft.db')
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            command = f"SELECT * FROM USER WHERE username = '{username}'"
            c.execute(command)
            user = get_user(username)

            if user is None:
                error = 'INCORRECT USERNAME'
            elif not check_password_hash(user['password'], password):
                error = 'INCORRECT PASSWORD'

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
                error = 'USER ALREADY REGISTERED.'
        except Exception as e:
            print(e)
            pass

        if error is None:
            try:
                create_user(user_dict)
                return {'message': 'REGISTERED'}, 200
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
                error = 'USER NOT FOUND.'
        except Exception as e:
            print('UPDATE USER ERROR', e)
            pass

        if error is None:
            try:
                update_user(user_dict)
                return 'UPDATE'
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    else:
        return {'message': ''}, 403

@app.route('/register_inst', methods=('GET','POST'))
@cross_origin(supports_credentials=True)
def register_inst():
    if request.method == 'POST':
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
        conn = create_connection('engsoft.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        error = None

        try:
            c.execute(f"SELECT * FROM INST WHERE nome = '{inst_dict['nome']}'")
            res = c.fetchall()
            if (len(res)>0):
                error = 'INST ALREADY REGISTERED.'
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

    else:
            return {'message': 'BAD REGISTER'}, 403

@app.route('/update_inst', methods=('GET','POST'))
@cross_origin(supports_credentials=True)
def _update_inst():
    if request.method == 'POST':
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
        conn = create_connection('engsoft.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        error = None    

        try:
            c.execute(f"SELECT * FROM INST WHERE id = '{inst_dict['id']}'")
            res = c.fetchall()
    
            if not (len(res)>0):
                error = 'INST NOT FOUND.'
        except Exception as e:
            print('UPDATE INST ERROR', e)
            pass

        if error is None:
            try:
                update_inst(inst_dict)
                return 'UPDATE'
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    else:
        return 'BAD UPDATE'

@app.route('/register_curs', methods=('GET','POST'))
@cross_origin(supports_credentials=True)
def register_curs():
    if request.method == 'POST':
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
        conn = create_connection('engsoft.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        error = None

        try:
            c.execute(f"SELECT * FROM CURS WHERE nome = '{curs_dict['nome']}' and inst_id = '{curs_dict['inst_id']}'")
            res = c.fetchall()
            print(len(res))
            if (len(res)>0):
                error = 'CURS ALREADY REGISTERED.'
        except Exception as e:
            print('CURS', e)
            pass

        if error is None:
            try:
                create_curs(curs_dict)
                return 'REGISTERED'
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    else:
        return 'BAD REGISTER'  

@app.route('/update_curs', methods=('GET','POST'))
@cross_origin(supports_credentials=True)
def _update_curs():
    if request.method == 'POST':
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
        conn = create_connection('engsoft.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        error = None    

        try:
            c.execute(f"SELECT * FROM CURS WHERE id = '{curs_dict['id']}'")
            res = c.fetchall()
    
            if not (len(res)>0):
                error = 'CURS NOT FOUND.'
        except Exception as e:
            print('UPDATE CURS ERROR', e)
            pass

        if error is None:
            try:
                update_curs(curs_dict)
                return 'UPDATE'
            except Exception as e:
                print('EXCEPTION', e)
        return {'message': error}, 403

    else:
        return 'BAD UPDATE'

if __name__ == "__main__":
    app.run(debug=True)