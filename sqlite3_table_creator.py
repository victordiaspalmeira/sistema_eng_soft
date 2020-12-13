import sqlite3 
from sqlite3 import Error
from sqlite3_manager import create_connection, create_user, create_inst
from werkzeug.security import generate_password_hash
def create_table_USER(conn):
    command = """ CREATE TABLE IF NOT EXISTS USER (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inst_id INTEGER,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    cargo TEXT NOT NULL
                );
                """
    try:
        c = conn.cursor()
        c.execute(command)
        conn.commit()
    except Error as e:
        print(e)

    return

def create_table_INST(conn):
    command = """ CREATE TABLE IF NOT EXISTS INST (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inst_type INTEGER,
                    visivel INTEGER,
                    nome TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    cidade TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    credenciamento TEXT NOT NULL,
                    mantenedora TEXT NOT NULL
                );
                """
    try:
        c = conn.cursor()
        c.execute(command)
        conn.commit()
    except Error as e:
        print(e)

def create_table_CURS(conn):
    command = """ CREATE TABLE IF NOT EXISTS CURS (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inst_id INTEGER,
                    nome TEXT NOT NULL,
                    grau TEXT NOT NULL,
                    codigo_emec TEXT NOT NULL,
                    ato_auto TEXT NOT NULL,
                    ato_reco TEXT NOT NULL,
                    ato_reno TEXT NOT NULL,
                    renov TEXT NOT NULL,
                    obs TEXT NOT NULL
                );
                """
    try:
        c = conn.cursor()
        c.execute(command)
        conn.commit()
    except Error as e:
        print(e)

def create_debug_user(conn):
    user_dict = {
        'inst_id': -1,
        'username': 'debug',
        'password': 'debug',
        'nome': 'debug',
        'sobrenome': 'debug',
        'telefone': '71 99999999',
        'email': 'debug@debug.com',
        'cargo': 'debug'
    }
    create_user(user_dict)
    #
    return 

if __name__ == "__main__":
    #Criação de tabela e usuário debug
    conn = create_connection('engsoft.db')
    #USER
    create_table_USER(conn)
    create_debug_user(conn)

    #INST
    create_table_INST(conn)

    #CURS
    create_table_CURS(conn)
