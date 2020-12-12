import sqlite3 
from sqlite3 import Error
from sqlite3_manager import create_connection, create_user
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

    return 

if __name__ == "__main__":
    conn = create_connection('engsoft.db')
    create_table_USER(conn)
    create_debug_user(conn)
