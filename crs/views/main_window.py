from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QPixmap
import os
from views.fornecedor_view import FornecedorView
from views.historico_view import HistoricoView
from views.produto_view import ProdutoView
from views.log_view import LogView
from controllers.relatorio_controller import RelatorioController
from controllers.notificacao_controller import NotificacaoController
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.relatorio_controller = RelatorioController(db)
        self.notificacao_controller = NotificacaoController(db)
        self.setWindowTitle("Sistema de Gerenciamento de Estoque")
        self.setGeometry(100, 100, 800, 500)

        # Criar o widget central que vai conter a imagem e os botões
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Criar um layout principal
        self.layout_principal = QVBoxLayout(self.central_widget)

        # Criar QLabel para exibir a imagem como fundo SOMENTE NA TELA PRINCIPAL
        self.background_label = QLabel(self.central_widget)
        logo_path = os.path.abspath("assets/logo.png")  # Caminho da imagem
        pixmap = QPixmap(logo_path)

        if pixmap.isNull():
            print(f"Erro ao carregar a imagem: {logo_path}")
        else:
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)  # Ajusta a imagem ao tamanho da tela
            self.background_label.lower()  # Manda a imagem para o fundo

        # Criar um widget para os botões e sobrepor à imagem
        self.button_widget = QWidget(self.central_widget)
        self.layout_botoes = QVBoxLayout(self.button_widget)

        self.btn_fornecedores = QPushButton("Gerenciar Fornecedores")
        self.btn_produtos = QPushButton("Gerenciar Produtos")
        self.btn_logs = QPushButton("Visualizar Logs")
        self.btn_relatorio_excel = QPushButton("Gerar Relatório Excel")
        self.btn_relatorio_pdf = QPushButton("Gerar Relatório PDF")
        self.btn_notificacoes = QPushButton("Verificar Notificações")

        # Definir tamanho fixo para os botões
        for btn in [self.btn_fornecedores, self.btn_produtos, self.btn_logs, self.btn_relatorio_excel, self.btn_relatorio_pdf, self.btn_notificacoes]:
            btn.setMinimumSize(200, 50)
            self.layout_botoes.addWidget(btn)

        # Conectar os botões às funções correspondentes
        self.btn_fornecedores.clicked.connect(self.abrir_fornecedor_view)
        self.btn_produtos.clicked.connect(self.abrir_produto_view)
        self.btn_logs.clicked.connect(self.abrir_log_view)
        self.btn_relatorio_excel.clicked.connect(lambda: self.gerar_relatorio("excel"))
        self.btn_relatorio_pdf.clicked.connect(lambda: self.gerar_relatorio("pdf"))
        self.btn_notificacoes.clicked.connect(self.notificacao_controller.exibir_notificacoes)

        # Adicionar os widgets ao layout principal
        self.layout_principal.addWidget(self.background_label)
        self.layout_principal.addWidget(self.button_widget)

        # Ajustar os tamanhos iniciais
        self.resizeEvent(None)

    def resizeEvent(self, event):
        """Redimensiona a imagem quando a janela for redimensionada"""
        self.background_label.resize(self.width(), self.height())
        self.button_widget.resize(self.width(), self.height())
        if event:
            event.accept()

    def abrir_fornecedor_view(self):
        self.fornecedor_view = FornecedorView(self.db)
        self.fornecedor_view.setStyleSheet("")  # REMOVE qualquer fundo herdado
        self.fornecedor_view.show()

    def abrir_produto_view(self):
        self.produto_view = ProdutoView(self.db)
        self.produto_view.setStyleSheet("")  # REMOVE qualquer fundo herdado
        self.produto_view.show()

    def abrir_log_view(self):
        self.log_view = LogView(self.db)
        self.log_view.setStyleSheet("")  # REMOVE qualquer fundo herdado
        self.log_view.show()

    def abrir_historico_view(self):
        self.historico_view = HistoricoView(self.db)
        self.historico_view.setStyleSheet("")  # REMOVE qualquer fundo herdado
        self.historico_view.show()
