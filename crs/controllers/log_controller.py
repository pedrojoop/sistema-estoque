# controllers/log_controller.py
import sqlite3
import json
from datetime import datetime

class LogController:
    def __init__(self, db):
        self.db = db

    def listar_logs(self, limite=50):
        """Retorna os logs das últimas alterações."""
        self.db.cursor.execute("SELECT * FROM logs ORDER BY data_hora DESC LIMIT ?", (limite,))
        logs = self.db.cursor.fetchall()
        log_list = []
        for log in logs:
            log_list.append({
                "id": log[0],
                "tipo_acao": log[1],
                "tabela": log[2],
                "id_alterado": log[3],
                "data_hora": log[4],
                "valor_anterior": json.loads(log[5]) if log[5] else None,
                "valor_novo": json.loads(log[6]) if log[6] else None
            })
        return log_list

    def buscar_log_por_id(self, log_id):
        """Retorna um log específico pelo ID."""
        self.db.cursor.execute("SELECT * FROM logs WHERE id=?", (log_id,))
        log = self.db.cursor.fetchone()
        if log:
            return {
                "id": log[0],
                "tipo_acao": log[1],
                "tabela": log[2],
                "id_alterado": log[3],
                "data_hora": log[4],
                "valor_anterior": json.loads(log[5]) if log[5] else None,
                "valor_novo": json.loads(log[6]) if log[6] else None
            }
        return None

    def limpar_logs_antigos(self, dias=30):
        """Remove logs mais antigos do que o número de dias especificado."""
        limite_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.cursor.execute("DELETE FROM logs WHERE data_hora < datetime(?, '-? days')", (limite_data, dias))
        self.db.conn.commit()