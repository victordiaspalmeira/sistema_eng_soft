import sqlite3
from sqlite3 import Error

def create_inst_table(conn):
    command = """ CREATE TABLE IF NOT EXISTS INST (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT NOT NULL,
                VISIVEL INTEGER NOT NULL,
                ENDERECO TEXT NOT NULL,
                CIDADE TEXT NOT NULL,
                ESTADO TEXT NOT NULL,
                CREDENCIAMENTO TEXT NOT NULL,
                MANTENEDORA TEXT NOT NULL
            );
            """
    try:
        c = conn.cursor()
        c.execute(command)
        return True
    except Error as e:
        print(e)
        return False

def create_inst_val_table(conn):
    command = """ CREATE TABLE IF NOT EXISTS INST (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT NOT NULL,
                VISIVEL INTEGER NOT NULL,
                ENDERECO TEXT NOT NULL,
                CIDADE TEXT NOT NULL,
                ESTADO TEXT NOT NULL,
                CREDENCIAMENTO TEXT NOT NULL,
                MANTENEDORA TEXT NOT NULL
            );
            """
    try:
        c = conn.cursor()
        c.execute(command)
        return True
    except Error as e:
        print(e)
        return False

def create_user_table(conn):
    command = """ CREATE TABLE IF NOT EXISTS USER (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                INST_ID INTEGER,
                INST_TYPE INTEGER,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                NOME TEXT NOT NULL,
                SOBRENOME TEXT NOT NULL,
                CARGO INTEGER,
                EMAIL TEXT NOT NULL,
                TELEFONE TEXT NOT NULL
            );
            """
    try:
        c = conn.cursor()
        c.execute(command)
        return True
    except Error as e:
        print(e)
        return False

def create_curso_table(conn):
    command = """ CREATE TABLE IF NOT EXISTS CURSO (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT NOT NULL,
                INST_ID INTEGER NOT NULL,
                CODIGO_EMEC INTEGER,
                ATO_AUTO TEXT NOT NULL,
                ATO_RECO TEXT NOT NULL,
                ATO_RENO TEXT NOT NULL,
                RENOVACOES BLOB,
                OBS TEXT
            );
            """
    try:
        c = conn.cursor()
        c.execute(command)
        return True
    except Error as e:
        print(e)
        return False

if __name__ == "__main__":
    conn = sqlite3.connect('engsoft.db') #open database
    create_inst_table(conn)
    create_inst_val_table(conn)
    create_user_table(conn)
    create_curso_table(conn)