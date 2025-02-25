# models/produto.py
from datetime import datetime

class Produto:
    def __init__(self, nome, fornecedor_id, valor, data_validade, quantidade, regiao):
        self.nome = nome
        self.fornecedor_id = fornecedor_id
        self.valor = valor
        self.data_validade = datetime.strptime(data_validade, "%Y-%m-%d")
        self.data_cadastro = datetime.now()
        self.data_atualizacao = datetime.now()
        self.quantidade = quantidade
        self.regiao = regiao

    def to_dict(self):
        return {
            "nome": self.nome,
            "fornecedor_id": self.fornecedor_id,
            "valor": self.valor,
            "data_validade": self.data_validade.strftime("%Y-%m-%d"),
            "data_cadastro": self.data_cadastro.strftime("%Y-%m-%d %H:%M:%S"),
            "data_atualizacao": self.data_atualizacao.strftime("%Y-%m-%d %H:%M:%S"),
            "quantidade": self.quantidade,
            "regiao": self.regiao
        }
