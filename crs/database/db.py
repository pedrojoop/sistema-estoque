# Atualizando a estrutura do banco de dados
import sqlite3

class Database:
    def __init__(self, db_name="estoque.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Criar tabela de Fornecedores
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            categoria TEXT NOT NULL,
            tipo_produto TEXT NOT NULL,
            regiao TEXT NOT NULL,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Criar tabela de Produtos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            fornecedor_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            regiao TEXT NOT NULL,
            data_validade DATETIME NOT NULL,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
        )
        ''')

        self.conn.commit()
    
    def close_connection(self):
        self.conn.close()