# Atualização no main.py para abrir a interface principal
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from database.db import Database
    from views.main_window import MainWindow

    db = Database()
    app = QApplication(sys.argv)
    main_window = MainWindow(db)
    main_window.show()
    sys.exit(app.exec_())