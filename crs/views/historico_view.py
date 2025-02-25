# views/historico_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from controllers.historico_controller import HistoricoController

class HistoricoView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.historico_controller = HistoricoController(self.db)
        self.setWindowTitle("Histórico de Ações")
        self.setGeometry(100, 100, 800, 400)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Usuário", "Ação", "Tabela", "Data e Hora"])
        layout.addWidget(self.table)
        
        self.btn_refresh = QPushButton("Atualizar Histórico")
        self.btn_refresh.clicked.connect(self.load_historico)
        layout.addWidget(self.btn_refresh)
        
        self.setLayout(layout)
        self.load_historico()

    def load_historico(self):
        historico = self.historico_controller.listar_historico()
        self.table.setRowCount(len(historico))
        for row_idx, acao in enumerate(historico):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(acao[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(acao[1]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(acao[2]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(acao[3]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(acao[5]))
