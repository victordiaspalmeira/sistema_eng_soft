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

