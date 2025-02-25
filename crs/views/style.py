import os

def get_stylesheet():
    logo_path = os.path.abspath("assets/logo.png").replace("\\", "/")  # Caminho absoluto da imagem

    return f"""
    QPushButton {{
        background-color: #555;
        border-radius: 5px;
        padding: 10px;
        color: white;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #777;
    }}
    QLineEdit, QComboBox {{
        background-color: #f0f0f0;
        border-radius: 5px;
        padding: 5px;
        color: black;
    }}
    """
