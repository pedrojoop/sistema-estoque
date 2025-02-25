# controllers/notificacao_controller.py
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox

class NotificacaoController:
    def __init__(self, db):
        self.db = db

    def verificar_estoque_baixo(self, limite=5):
        """Verifica produtos com estoque abaixo do limite e retorna notificações."""
        self.db.cursor.execute("SELECT nome, quantidade FROM produtos WHERE quantidade <= ?", (limite,))
        produtos = self.db.cursor.fetchall()
        notificacoes = [f"Produto '{p[0]}' está com estoque baixo ({p[1]} unidades)" for p in produtos]
        return notificacoes

    def verificar_produtos_vencendo(self, dias=7):
        """Verifica produtos com data de validade próxima e retorna notificações."""
        data_limite = (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d")
        self.db.cursor.execute("SELECT nome, data_validade FROM produtos WHERE data_validade <= ?", (data_limite,))
        produtos = self.db.cursor.fetchall()
        notificacoes = [f"Produto '{p[0]}' vence em {p[1]}" for p in produtos]
        return notificacoes

    def exibir_notificacoes(self):
        """Exibe notificações de estoque baixo e produtos vencendo."""
        notificacoes = self.verificar_estoque_baixo() + self.verificar_produtos_vencendo()
        if notificacoes:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Notificações de Estoque")
            msg.setText("\n".join(notificacoes))
            msg.exec_()