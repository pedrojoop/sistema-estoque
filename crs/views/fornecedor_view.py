# views/fornecedor_view.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QFormLayout, QMessageBox, QComboBox
from controllers.fornecedor_controller import FornecedorController
from views.style import get_stylesheet

class FornecedorView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.fornecedor_controller = FornecedorController(self.db)
        self.setWindowTitle("Gerenciamento de Fornecedores")
        self.setGeometry(100, 100, 900, 450)
        self.setStyleSheet(get_stylesheet())
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Pesquisar fornecedor...")
        self.filter_input.textChanged.connect(self.load_fornecedores)
        layout.addWidget(self.filter_input)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["ID", "Nome", "CNPJ", "Categoria", "Tipo de Produto", "Região"])
        self.sort_combo.currentIndexChanged.connect(self.load_fornecedores)
        layout.addWidget(self.sort_combo)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CNPJ", "Categoria", "Tipo de Produto", "Região"])
        layout.addWidget(self.table)
        
        self.btn_add = QPushButton("Adicionar Fornecedor")
        self.btn_add.clicked.connect(self.adicionar_fornecedor)
        layout.addWidget(self.btn_add)
        
        self.btn_edit = QPushButton("Editar Fornecedor")
        self.btn_edit.clicked.connect(self.editar_fornecedor)
        layout.addWidget(self.btn_edit)
        
        self.btn_refresh = QPushButton("Atualizar Fornecedores")
        self.btn_refresh.clicked.connect(self.load_fornecedores)
        layout.addWidget(self.btn_refresh)
        
        self.btn_delete = QPushButton("Excluir Fornecedor")
        self.btn_delete.clicked.connect(self.excluir_fornecedor)
        layout.addWidget(self.btn_delete)
        
        self.setLayout(layout)
        self.load_fornecedores()

    def load_fornecedores(self):
        fornecedores = self.fornecedor_controller.listar_fornecedores()
        self.table.setRowCount(len(fornecedores))
        for row_idx, fornecedor in enumerate(fornecedores):
            for col_idx, value in enumerate(fornecedor):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
    
    def adicionar_fornecedor(self):
        self.add_window = QWidget()
        self.add_window.setWindowTitle("Adicionar Fornecedor")
        self.add_window.setGeometry(200, 200, 400, 250)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.cnpj_input = QLineEdit()
        self.categoria_input = QLineEdit()
        self.tipo_produto_input = QLineEdit()
        self.regiao_input = QLineEdit()
                
        form_layout.addRow(QLabel("Nome:"), self.nome_input)
        form_layout.addRow(QLabel("CNPJ:"), self.cnpj_input)
        form_layout.addRow(QLabel("Categoria:"), self.categoria_input)
        form_layout.addRow(QLabel("Tipo de Produto:"), self.tipo_produto_input)
        form_layout.addRow(QLabel("Região:"), self.regiao_input)
        
        self.btn_save = QPushButton("Salvar")
        self.btn_save.clicked.connect(self.salvar_fornecedor)
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_save)
        
        self.add_window.setLayout(layout)
        self.add_window.show()

    def editar_fornecedor(self):
        selected = self.table.currentRow()
        if selected >= 0:
            fornecedor_id = int(self.table.item(selected, 0).text())
            self.edit_window = QWidget()
            self.edit_window.setWindowTitle("Editar Fornecedor")
            self.edit_window.setGeometry(200, 200, 400, 250)
            
            layout = QVBoxLayout()
            form_layout = QFormLayout()
            
            self.nome_input = QLineEdit(self.table.item(selected, 1).text())
            self.cnpj_input = QLineEdit(self.table.item(selected, 2).text())
            self.categoria_input = QLineEdit(self.table.item(selected, 3).text())
            self.tipo_produto_input = QLineEdit(self.table.item(selected, 4).text())
            self.regiao_input = QLineEdit(self.table.item(selected, 5).text())
            
            form_layout.addRow(QLabel("Nome:"), self.nome_input)
            form_layout.addRow(QLabel("CNPJ:"), self.cnpj_input)
            form_layout.addRow(QLabel("Categoria:"), self.categoria_input)
            form_layout.addRow(QLabel("Tipo de Produto:"), self.tipo_produto_input)
            form_layout.addRow(QLabel("Região:"), self.regiao_input)
            
            self.btn_save = QPushButton("Salvar")
            self.btn_save.clicked.connect(lambda: self.salvar_edicao_fornecedor(fornecedor_id))
            layout.addLayout(form_layout)
            layout.addWidget(self.btn_save)
            
            self.edit_window.setLayout(layout)
            self.edit_window.show()
    
    def salvar_edicao_fornecedor(self, fornecedor_id):
        nome = self.nome_input.text()
        cnpj = self.cnpj_input.text()
        categoria = self.categoria_input.text()
        tipo_produto = self.tipo_produto_input.text()
        regiao = self.regiao_input.text()
        
        if nome and cnpj:
            self.fornecedor_controller.atualizar_fornecedor(fornecedor_id, nome, cnpj, categoria, tipo_produto, regiao)
            self.load_fornecedores()
            self.edit_window.close()
        else:
            QMessageBox.warning(self, "Erro", "Nome e CNPJ são obrigatórios.")  
        
    def salvar_fornecedor(self):
        nome = self.nome_input.text()
        cnpj = self.cnpj_input.text()
        categoria = self.categoria_input.text()
        tipo_produto = self.tipo_produto_input.text()
        regiao = self.regiao_input.text()
        
        if nome and cnpj:
            self.fornecedor_controller.adicionar_fornecedor(nome, cnpj, categoria, tipo_produto, regiao)
            self.load_fornecedores()
            self.add_window.close()
        else:
            QMessageBox.warning(self, "Erro", "Nome e CNPJ são obrigatórios.")

    def excluir_fornecedor(self):
        selected = self.table.currentRow()
        if selected >= 0:
            fornecedor_id = int(self.table.item(selected, 0).text())
            confirm = QMessageBox.question(self, "Excluir Fornecedor", "Tem certeza que deseja excluir este fornecedor?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.fornecedor_controller.deletar_fornecedor(fornecedor_id)
                self.load_fornecedores()
                