# models/fornecedor.py
from datetime import datetime

class Fornecedor:
    def __init__(self, nome, cnpj, categoria, tipo_produto, regiao):
        self.nome = nome
        self.cnpj = cnpj
        self.categoria = categoria
        self.tipo_produto = tipo_produto
        self.regiao = regiao
        self.data_cadastro = datetime.now()

    def to_dict(self):
        return {
            "nome": self.nome,
            "cnpj": self.cnpj,
            "categoria": self.categoria,
            "tipo_produto": self.tipo_produto,
            "regiao": self.regiao,
            "data_cadastro": self.data_cadastro.strftime("%Y-%m-%d %H:%M:%S")
        }
