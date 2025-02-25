# views/log_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from controllers.log_controller import LogController

class LogView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.log_controller = LogController(self.db)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Painel de Auditoria - Logs")
        self.setGeometry(100, 100, 800, 400)

        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Ação", "Tabela", "ID Alterado", "Data e Hora", "Detalhes"])
        layout.addWidget(self.table)
        
        self.load_logs()
        
        self.btn_refresh = QPushButton("Atualizar Logs")
        self.btn_refresh.clicked.connect(self.load_logs)
        layout.addWidget(self.btn_refresh)
        
        self.setLayout(layout)

    def load_logs(self):
        logs = self.log_controller.listar_logs()
        self.table.setRowCount(len(logs))
        for row_idx, log in enumerate(logs):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(log["id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(log["tipo_acao"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(log["tabela"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(log["id_alterado"])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(log["data_hora"]))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(log["valor_anterior"])) if log["valor_anterior"] else QTableWidgetItem("-"))