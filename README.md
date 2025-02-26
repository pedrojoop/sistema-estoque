# 📦 Sistema de Gerenciamento de Estoque

## 📌 Descrição
Este é um sistema de gerenciamento de estoque desenvolvido em **Python** com **PyQt5** e **SQLite**. Ele permite cadastrar, editar e excluir **fornecedores** e **produtos**, armazenando informações como **nome, CNPJ, categoria, tipo de produto, região, data de validade e data de cadastro**.

O sistema também gera **relatórios em Excel e PDF**, além de manter um **log de alterações** para permitir a reversão de modificações.

## 🚀 Funcionalidades
- 📌 **Cadastro de Fornecedores**
  - Nome, CNPJ, Categoria, Tipo de Produto, Região
- 📦 **Cadastro de Produtos**
  - Nome, Fornecedor, Valor, Quantidade, Região, Data de Validade, Data de Cadastro
- 📊 **Geração de Relatórios**
  - Exporta dados para **Excel** e **PDF**
- 🔄 **Log de Operações**
  - Registra modificações e permite **desfazer alterações**
- 📅 **Seleção de Data**
  - Campo de **calendário** para facilitar a seleção de data de validade

---

## 🛠️ Instalação

### 1️⃣ Clonar o repositório
```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
```

### 2️⃣ Criar ambiente virtual
```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
```

### 3️⃣ Instalar dependências
```bash
    pip install -r requirements.txt
```

### 4️⃣ Executar o sistema
```bash
    python main.py
```

---

## 📁 Estrutura do Projeto
```
📂 projeto
├── 📁 controllers
│   ├── fornecedor_controller.py
│   ├── produto_controller.py
├── 📁 models
│   ├── fornecedor.py
│   ├── produto.py
├── 📁 views
│   ├── main_window.py
│   ├── fornecedor_view.py
│   ├── produto_view.py
├── 📁 database
│   ├── db.py
├── 📂 assets
│   ├── logo.png
├── main.py
├── README.md
├── requirements.txt
```

---

## 📜 Uso do Sistema
1️⃣ **Executar o sistema**: Abra o terminal e rode `python main.py`.
2️⃣ **Cadastrar fornecedores**: No menu principal, clique em "Gerenciar Fornecedores" e preencha os campos.
3️⃣ **Cadastrar produtos**: Acesse "Gerenciar Produtos" e preencha as informações.
4️⃣ **Gerar relatórios**: Clique em "Gerar Relatório Excel" ou "Gerar Relatório PDF".
5️⃣ **Reverter alterações**: Acesse "Log" para desfazer a última modificação.

---

## 📝 Tecnologias Utilizadas
- Python 🐍
- PyQt5 🖥️
- SQLite 🗃️
- Pandas 📊
- ReportLab 📝

---

## 🤝 Contribuição
Se quiser contribuir:
1. **Fork** o repositório
2. Crie uma **branch** com a nova funcionalidade (`git checkout -b minha-feature`)
3. **Commit** suas alterações (`git commit -m 'Adicionando nova funcionalidade'`)
4. **Push** a branch (`git push origin minha-feature`)
5. Abra um **Pull Request** 🚀

---

Feito com ❤️ por [Pedro Matheus](https://github.com/pedrojoop) 🚀

