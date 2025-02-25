# controllers/historico_controller.py
import sqlite3
from datetime import datetime

class HistoricoController:
    def __init__(self, db):
        self.db = db
        self.criar_tabela_historico()

    def criar_tabela_historico(self):
        """Cria a tabela de histórico de ações se não existir."""
        self.db.cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            acao TEXT NOT NULL,
            tabela TEXT NOT NULL,
            id_alterado INTEGER NOT NULL,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.db.conn.commit()

    def registrar_acao(self, usuario, acao, tabela, id_alterado):
        """Registra uma ação no histórico."""
        self.db.cursor.execute('''
        INSERT INTO historico (usuario, acao, tabela, id_alterado, data_hora)
        VALUES (?, ?, ?, ?, ?)''',
        (usuario, acao, tabela, id_alterado, datetime.now()))
        self.db.conn.commit()

    def listar_historico(self, limite=50):
        """Retorna as últimas ações registradas no histórico."""
        self.db.cursor.execute("SELECT * FROM historico ORDER BY data_hora DESC LIMIT ?", (limite,))
        return self.db.cursor.fetchall()