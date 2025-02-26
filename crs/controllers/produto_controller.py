# controllers/produto_controller.py
import psycopg2
import json
from datetime import datetime

class ProdutoController:
    def __init__(self, db):
        self.db = db

    def adicionar_produto(self, nome, fornecedor_id, valor, quantidade, regiao, data_validade):
        self.db.cursor.execute(
            '''INSERT INTO produtos (nome, fornecedor_id, valor, quantidade, regiao, data_validade, data_cadastro)
               VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)''',
            (nome, fornecedor_id, valor, quantidade, regiao, data_validade)
        )
        self.db.conn.commit()

    def listar_produtos(self):
        self.db.cursor.execute("SELECT id, nome, fornecedor_id, valor, quantidade, regiao, data_validade, data_cadastro FROM produtos;")
        return self.db.cursor.fetchall()
    
    def atualizar_produto(self, produto_id, nome, fornecedor_id, valor, quantidade, regiao, data_validade):
        self.db.cursor.execute("SELECT * FROM produtos WHERE id=%s;", (produto_id,))
        old_data = self.db.cursor.fetchone()
        
        self.db.cursor.execute('''UPDATE produtos 
                                  SET nome=%s, fornecedor_id=%s, valor=%s, quantidade=%s, regiao=%s, data_validade=%s, data_cadastro=CURRENT_TIMESTAMP
                                  WHERE id=%s''',
                               (nome, fornecedor_id, valor, quantidade, regiao, data_validade, produto_id))
        self.db.conn.commit()

        self.registrar_log("UPDATE", "produtos", produto_id, {
            "nome": nome,
            "fornecedor_id": fornecedor_id,
            "valor": valor,
            "quantidade": quantidade,
            "regiao": regiao,
            "data_validade": data_validade
        })

    def deletar_produto(self, produto_id):
        self.db.cursor.execute("SELECT * FROM produtos WHERE id=%s;", (produto_id,))
        old_data = self.db.cursor.fetchone()
        
        self.db.cursor.execute("DELETE FROM produtos WHERE id=%s;", (produto_id,))
        self.db.conn.commit()

        self.registrar_log("DELETE", "produtos", produto_id, old_data, None)

    def registrar_log(self, acao, tabela, id_alterado, valor_anterior, valor_novo):
        self.db.cursor.execute('''INSERT INTO logs (tipo_acao, tabela, id_alterado, data_hora, valor_anterior, valor_novo)
                                  VALUES (%s, %s, %s, %s, %s, %s)''',
                               (acao, tabela, id_alterado, datetime.now(), json.dumps(valor_anterior), json.dumps(valor_novo)))
        self.db.conn.commit()

        
    def desfazer_ultima_alteracao(self):
        self.db.cursor.execute("SELECT * FROM logs ORDER BY data_hora DESC LIMIT 1")
        ultimo_log = self.db.cursor.fetchone()
        if not ultimo_log:
            return "Nenhuma alteração para reverter."

        acao, tabela, id_alterado, _, valor_anterior, valor_novo = ultimo_log[1:]
        
        if acao == "INSERT":
            self.db.cursor.execute(f"DELETE FROM {tabela} WHERE id=?", (id_alterado,))
        elif acao == "DELETE":
            dados = json.loads(valor_anterior)
            colunas = ", ".join(dados.keys())
            valores = tuple(dados.values())
            placeholders = ", ".join(["?" for _ in dados])
            self.db.cursor.execute(f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})", valores)
        elif acao == "UPDATE":
            dados = json.loads(valor_anterior)
            set_clause = ", ".join([f"{key}=?" for key in dados.keys()])
            valores = tuple(dados.values()) + (id_alterado,)
            self.db.cursor.execute(f"UPDATE {tabela} SET {set_clause} WHERE id=?", valores)
        
        self.db.conn.commit()
        self.db.cursor.execute("DELETE FROM logs WHERE id=?", (ultimo_log[0],))
        self.db.conn.commit()
        return "Última alteração revertida com sucesso."