# controllers/relatorio_controller.py
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog
from fpdf import FPDF

class RelatorioController:
    def __init__(self, db):
        self.db = db

    def gerar_relatorio_excel(self, tabela):
        """Gera um relatório formatado em Excel, incluindo estatísticas."""
        self.db.cursor.execute(f"SELECT * FROM {tabela}")
        dados = self.db.cursor.fetchall()
        colunas = [desc[0] for desc in self.db.cursor.description]
        
        df = pd.DataFrame(dados, columns=colunas)
        
        # Estatísticas básicas
        estatisticas = df.describe()
        
        writer = pd.ExcelWriter("relatorio.xlsx", engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Relatório", index=False)
        estatisticas.to_excel(writer, sheet_name="Estatísticas")
        
        workbook = writer.book
        worksheet = writer.sheets["Relatório"]
        
        for i, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_length)
        
        writer.close()
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Salvar Relatório", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_path:
            df.to_excel(file_path, index=False)
            return "Relatório Excel salvo com sucesso!"
        return "Operação cancelada pelo usuário."

    def gerar_relatorio_pdf(self, tabela):
        """Gera um relatório formatado em PDF, incluindo estatísticas e gráficos."""
        self.db.cursor.execute(f"SELECT * FROM {tabela}")
        dados = self.db.cursor.fetchall()
        colunas = [desc[0] for desc in self.db.cursor.description]
        
        df = pd.DataFrame(dados, columns=colunas)
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        
        pdf.cell(200, 10, f"Relatório de {tabela.capitalize()}", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", style="B", size=10)
        cell_width = 190 // len(colunas)
        
        for coluna in colunas:
            pdf.cell(cell_width, 10, coluna, border=1, align="C")
        pdf.ln()
        
        pdf.set_font("Arial", size=9)
        for linha in dados:
            for item in linha:
                pdf.cell(cell_width, 10, str(item), border=1, align="C")
            pdf.ln()
        
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, "Estatísticas do Estoque", ln=True, align="C")
        pdf.ln(10)
        
        estatisticas = df.describe().to_string()
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, estatisticas)
        
        fig, ax = plt.subplots()
        df["quantidade"].hist(bins=10, ax=ax)
        ax.set_title("Distribuição de Quantidade no Estoque")
        ax.set_xlabel("Quantidade")
        ax.set_ylabel("Frequência")
        
        grafico_path = "grafico.png"
        plt.savefig(grafico_path)
        pdf.add_page()
        pdf.image(grafico_path, x=10, w=180)
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Salvar Relatório", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_path:
            pdf.output(file_path)
            return "Relatório PDF salvo com sucesso!"
        return "Operação cancelada pelo usuário."