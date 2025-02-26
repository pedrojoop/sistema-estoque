# controllers/fornecedor_controller.py
import psycopg2
import json
from datetime import datetime

class FornecedorController:
    def __init__(self, db):
        self.db = db

    def adicionar_fornecedor(self, nome, cnpj, categoria, tipo_produto, regiao):
        self.db.cursor.execute(
            '''INSERT INTO fornecedores (nome, cnpj, categoria, tipo_produto, regiao, data_cadastro)
               VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)''',
            (nome, cnpj, categoria, tipo_produto, regiao)
        )
        self.db.conn.commit()
        
    def listar_fornecedores(self):
        self.db.cursor.execute("SELECT id, nome, cnpj, categoria, tipo_produto, regiao, data_cadastro FROM fornecedores;")
        return self.db.cursor.fetchall()
    
    def atualizar_fornecedor(self, fornecedor_id, nome, cnpj, categoria, tipo_produto, regiao):
        self.db.cursor.execute("SELECT * FROM fornecedores WHERE id=%s;", (fornecedor_id,))
        old_data = self.db.cursor.fetchone()
        
        self.db.cursor.execute('''UPDATE fornecedores 
                                  SET nome=%s, cnpj=%s, categoria=%s, tipo_produto=%s, regiao=%s, data_cadastro=CURRENT_TIMESTAMP 
                                  WHERE id=%s''',
                               (nome, cnpj, categoria, tipo_produto, regiao, fornecedor_id))
        self.db.conn.commit()
        
        self.registrar_log("UPDATE", "fornecedores", fornecedor_id, {
            "nome": nome,
            "cnpj": cnpj,
            "categoria": categoria,
            "tipo_produto": tipo_produto,
            "regiao": regiao
        })

    def deletar_fornecedor(self, fornecedor_id):
        self.db.cursor.execute("SELECT * FROM fornecedores WHERE id=%s;", (fornecedor_id,))
        old_data = self.db.cursor.fetchone()
        
        self.db.cursor.execute("DELETE FROM fornecedores WHERE id=%s;", (fornecedor_id,))
        self.db.conn.commit()
        
        self.registrar_log("DELETE", "fornecedores", fornecedor_id, old_data, None)

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
