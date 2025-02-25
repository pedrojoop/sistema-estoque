# views/produto_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QFormLayout, QMessageBox, QComboBox, QDateEdit
from controllers.produto_controller import ProdutoController
from PyQt5.QtCore import QDate
from controllers.fornecedor_controller import FornecedorController
from views.style import get_stylesheet

class ProdutoView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.produto_controller = ProdutoController(self.db)
        self.fornecedor_controller = FornecedorController(self.db)
        self.setWindowTitle("Gerenciamento de Produtos")
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet(get_stylesheet())
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Pesquisar produto...")
        self.filter_input.textChanged.connect(self.load_produtos)
        layout.addWidget(self.filter_input)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["ID", "Nome", "Fornecedor ID", "Valor", "Quantidade", "Região", "Data de Validade", "Data de Cadastro"])
        self.sort_combo.currentIndexChanged.connect(self.load_produtos)
        layout.addWidget(self.sort_combo)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "Fornecedor ID", "Valor", "Quantidade", "Região", "Data de Validade", "Data de Cadastro"])
        layout.addWidget(self.table)
        
        self.btn_add = QPushButton("Adicionar Produto")
        self.btn_add.clicked.connect(self.adicionar_produto)
        layout.addWidget(self.btn_add)
        
        self.btn_edit = QPushButton("Editar Produto")
        self.btn_edit.clicked.connect(self.editar_produto)
        layout.addWidget(self.btn_edit)
        
        self.btn_delete = QPushButton("Excluir Produto")
        self.btn_delete.clicked.connect(self.excluir_produto)
        layout.addWidget(self.btn_delete)
        
        self.btn_refresh = QPushButton("Atualizar Produtos")
        self.btn_refresh.clicked.connect(self.load_produtos)
        layout.addWidget(self.btn_refresh)
        
        self.setLayout(layout)
        self.load_produtos()

    def load_produtos(self):
        produtos = self.produto_controller.listar_produtos()
        self.table.setRowCount(len(produtos))
        for row_idx, produto in enumerate(produtos):
            for col_idx, value in enumerate(produto):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
    
    def adicionar_produto(self):
        self.add_window = QWidget()
        self.add_window.setWindowTitle("Adicionar Produto")
        self.add_window.setGeometry(200, 200, 400, 250)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.fornecedor_input = QComboBox()
        self.valor_input = QLineEdit()
        self.quantidade_input = QLineEdit()
        self.regiao_input = QLineEdit()
        self.data_validade_input = QLineEdit()
        
        # Campo de Data de Validade com seletor de calendário
        self.data_validade_input = QDateEdit()
        self.data_validade_input.setCalendarPopup(True)
        self.data_validade_input.setDisplayFormat("dd/MM/yyyy")
        self.data_validade_input.setDate(QDate.currentDate())
        
        # Carregar lista de fornecedores
        fornecedores = self.fornecedor_controller.listar_fornecedores()
        self.fornecedor_map = {}
        for fornecedor in fornecedores:
            self.fornecedor_map[fornecedor[1]] = fornecedor[0]  # Nome -> ID
            self.fornecedor_input.addItem(fornecedor[1])
        
        form_layout.addRow(QLabel("Nome:"), self.nome_input)
        form_layout.addRow(QLabel("Fornecedor:"), self.fornecedor_input)
        form_layout.addRow(QLabel("Valor:"), self.valor_input)
        form_layout.addRow(QLabel("Quantidade:"), self.quantidade_input)
        form_layout.addRow(QLabel("Região:"), self.regiao_input)
        form_layout.addRow(QLabel("Data de Validade:"), self.data_validade_input)
        
        self.btn_save = QPushButton("Salvar")
        self.btn_save.clicked.connect(self.salvar_produto)
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_save)
        
        self.add_window.setLayout(layout)
        self.add_window.show()
        
    def salvar_produto(self):
        nome = self.nome_input.text()
        fornecedor_nome = self.fornecedor_input.currentText()
        fornecedor_id = self.fornecedor_map[fornecedor_nome]
        valor = float(self.valor_input.text())
        quantidade = int(self.quantidade_input.text())
        regiao = self.regiao_input.text()
        data_validade = self.data_validade_input.date().toString("yyyy-MM-dd")
        
        if nome and fornecedor_id:
            self.produto_controller.adicionar_produto(nome, fornecedor_id, valor, data_validade, quantidade, regiao)
            self.load_produtos()
            self.add_window.close()
        else:
            QMessageBox.warning(self, "Erro", "Nome e Fornecedor são obrigatórios.")



    def editar_produto(self):
        selected = self.table.currentRow()
        if selected >= 0:
            produto_id = int(self.table.item(selected, 0).text())
            self.edit_window = QWidget()
            self.edit_window.setWindowTitle("Editar Produto")
            self.edit_window.setGeometry(200, 200, 400, 200)
            
            layout = QVBoxLayout()
            form_layout = QFormLayout()
            
            self.nome_input = QLineEdit(self.table.item(selected, 1).text())
            self.valor_input = QLineEdit(self.table.item(selected, 3).text())
            self.quantidade_input = QLineEdit(self.table.item(selected, 4).text())
            
            form_layout.addRow(QLabel("Nome:"), self.nome_input)
            form_layout.addRow(QLabel("Valor:"), self.valor_input)
            form_layout.addRow(QLabel("Quantidade:"), self.quantidade_input)
            
            self.btn_save = QPushButton("Salvar")
            self.btn_save.clicked.connect(lambda: self.salvar_edicao_produto(produto_id))
            layout.addLayout(form_layout)
            layout.addWidget(self.btn_save)
            
            self.edit_window.setLayout(layout)
            self.edit_window.show()
    
    def salvar_edicao_produto(self, produto_id):
        nome = self.nome_input.text()
        valor = self.valor_input.text()
        quantidade = self.quantidade_input.text()
        
        if nome and valor:
            self.produto_controller.atualizar_produto(produto_id, nome, 1, valor, "2025-12-31", quantidade)
            self.load_produtos()
            self.edit_window.close()
        else:
            QMessageBox.warning(self, "Erro", "Nome e Valor são obrigatórios.")

    def excluir_produto(self):
        selected = self.table.currentRow()
        if selected >= 0:
            produto_id = int(self.table.item(selected, 0).text())
            confirm = QMessageBox.question(self, "Excluir Produto", "Tem certeza que deseja excluir este produto?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.produto_controller.deletar_produto(produto_id)
                self.load_produtos()