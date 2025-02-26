import psycopg2
from psycopg2 import sql
from datetime import datetime

class Database:
    def __init__(self, db_name="estoque", user="postgres", password="2303", host="localhost", port="5432"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS fornecedores (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            categoria TEXT NOT NULL,
            tipo_produto TEXT NOT NULL,
            regiao TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            fornecedor_id INTEGER NOT NULL REFERENCES fornecedores(id) ON DELETE CASCADE,
            valor REAL NOT NULL,
            data_validade DATE NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            quantidade INTEGER NOT NULL,
            regiao TEXT
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            tipo_acao TEXT NOT NULL,
            tabela TEXT NOT NULL,
            id_alterado INTEGER NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            valor_anterior TEXT,
            valor_novo TEXT
        );
        ''')
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
