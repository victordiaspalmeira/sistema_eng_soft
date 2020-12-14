import sqlite3 
from sqlite3 import Error
from werkzeug.security import check_password_hash, generate_password_hash

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print('\n\n\n\n\n\n\nERROR CONNECTION', e)

def get_user(username=None, id=None):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if username is not None:
        command = f"SELECT * FROM USER WHERE username = '{username}'"
    elif id is not None:
        command = f"SELECT * FROM USER WHERE id = '{id}'"
    c.execute(command)
    user = c.fetchone()
    return user

def get_all_users(cargo, inst_id=None):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    #Filtragem por cargo
    #1. Se for diretor, só poder ver usuários
    if cargo.lower() == 'diretor':
        command = f"SELECT * FROM USER WHERE inst_id = '{inst_id}'"
    elif cargo.lower() in ['superintendente', 'debug']:
        command = f"SELECT * FROM USER"
    else:
        return 'None'

    c.execute(command)
    user_list = list()
    for user in c.fetchall():
        user_list.append(user)
    return user_list

def create_user(user_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"INSERT INTO USER (inst_id, username, password, nome, sobrenome, telefone, email, cargo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    values = (
        user_dict['inst_id'],
        user_dict['username'],
        generate_password_hash(user_dict['password']),
        user_dict['nome'],
        user_dict['sobrenome'],
        user_dict['telefone'],
        user_dict['email'],
        user_dict['cargo']
    )
    c.execute(command, values)    
    conn.commit()

    return

def update_user(user_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"UPDATE USER SET inst_id = '{user_dict['inst_id']}', nome = '{user_dict['nome']}', sobrenome = '{user_dict['sobrenome']}', telefone = '{user_dict['telefone']}', email = '{user_dict['email']}', cargo = '{user_dict['cargo']}' WHERE id = '{user_dict['id']}'"

    c.execute(command)    
    conn.commit()

    return

def remove_user(user_id):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"DELETE FROM USER WHERE id = {user_id}"

    c.execute(command)    
    conn.commit()

    return
        

def get_inst(nome=None, id=None):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if nome is not None:
        command = f"SELECT * FROM INST WHERE nome = '{nome}'"
    elif id is not None:
        command = f"SELECT * FROM INST WHERE id = '{id}'"
    c.execute(command)
    inst = c.fetchone()
    return inst

def get_all_insts(cargo):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if(cargo.lower() in ['superintendente', 'debug']):
        command = f"SELECT * FROM INST"
    else:
        command = f"SELECT * FROM INST  WHERE visivel = '1'"
    c.execute(command)

    return c.fetchall()  

def create_inst(inst_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"INSERT INTO INST (inst_type, visivel, nome, endereco, cidade, estado, credenciamento, mantenedora) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    values = (
        inst_dict['inst_type'],
        inst_dict['visivel'],
        inst_dict['nome'],
        inst_dict['endereco'],
        inst_dict['cidade'],
        inst_dict['estado'],
        inst_dict['credenciamento'],
        inst_dict['mantenedora'],
    )
    c.execute(command, values)    
    conn.commit()

    return

def update_inst(inst_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"UPDATE INST SET inst_type = '{inst_dict['inst_type']}', visivel = '{inst_dict['visivel']}', nome = '{inst_dict['nome']}', endereco = '{inst_dict['endereco']}', cidade = '{inst_dict['cidade']}', estado = '{inst_dict['estado']}', credenciamento = '{inst_dict['credenciamento']}', mantenedora = '{inst_dict['mantenedora']}' WHERE id = '{inst_dict['id']}'"

    c.execute(command)    
    conn.commit()

    return

def get_curs(curs_id):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    command = f"SELECT * FROM CURS WHERE id = '{curs_id}'"
    c.execute(command)
    curs = c.fetchone()

    return curs

def get_all_curs(inst_id):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    command = f"SELECT * FROM CURS WHERE inst_id = '{inst_id}'"
    c.execute(command)
    curs = c.fetchall()

    return curs

def create_curs(curs_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"INSERT INTO CURS (inst_id, nome, grau, codigo_emec, ato_auto, ato_reco, ato_reno, renov, obs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (
        curs_dict['inst_id'],
        curs_dict['nome'],
        curs_dict['grau'],
        curs_dict['codigo_emec'],
        curs_dict['ato_auto'],
        curs_dict['ato_reco'],
        curs_dict['ato_reno'],
        curs_dict['renov'],
        curs_dict['obs']
    )
    c.execute(command, values)    
    conn.commit()

    return

def update_curs(curs_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"UPDATE CURS SET nome = '{curs_dict['nome']}', grau = '{curs_dict['grau']}', codigo_emec = '{curs_dict['codigo_emec']}', ato_auto = '{curs_dict['ato_auto']}', ato_reco = '{curs_dict['ato_reco']}', ato_reno = '{curs_dict['ato_reno']}', renov = '{curs_dict['renov']}', obs = '{curs_dict['obs']}' WHERE id = '{curs_dict['id']}'"

    c.execute(command)    
    conn.commit()

    return

def get_user_cargo(user_id):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"SELECT cargo from USER where ID = '{user_id}'"

    c.execute(command)    
    return c.fetchone()[0]