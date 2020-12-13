import sqlite3 
from sqlite3 import Error

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

def get_user(username):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    command = f"SELECT * FROM USER WHERE username = '{username}'"
    c.execute(command)

    return c.fetchone()

def create_user(user_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"INSERT INTO USER (inst_id, username, password, nome, sobrenome, telefone, email, cargo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    values = (
        user_dict['inst_id'],
        user_dict['username'],
        user_dict['password'],
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

def get_inst(nome):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    command = f"SELECT * FROM INST WHERE nome = '{username}'"
    c.execute(command)

    return c.fetchone()    

def create_inst(inst_dict):
    conn = create_connection('engsoft.db')
    c = conn.cursor()
    command = f"INSERT INTO INST (inst_type, nome, endereco, cidade, estado, credenciamento, mantenedora) VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (
        inst_dict['inst_type'],
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

def get_curs(nome, curs_id):
    conn = create_connection('engsoft.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    command = f"SELECT * FROM CURS WHERE nome = '{username}' AND inst_id = '{inst_id}'"
    c.execute(command)

    return c.fetchone() 

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
