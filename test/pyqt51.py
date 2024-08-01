import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox

class MenuExample(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PyQt5 Menu Example")

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.on_open)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.on_save)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.setGeometry(300, 300, 400, 300)

    def on_open(self):
        QMessageBox.information(self, "Menu", "Open clicked")

    def on_save(self):
        QMessageBox.information(self, "Menu", "Save clicked")

def main():
    app = QApplication(sys.argv)
    ex = MenuExample()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
