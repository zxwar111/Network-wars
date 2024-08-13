import os
import sys
import subprocess
import paramiko
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QMessageBox, QInputDialog, QListWidget,
    QVBoxLayout, QWidget, QTextEdit, QDockWidget, QPushButton, QHBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
)
from PyQt5.QtCore import Qt, QRectF, QTimer
from PyQt5.QtGui import QBrush, QColor

# Setup Game Directory
NETWORK_ROOT = "NetworkRoot"
if not os.path.exists(NETWORK_ROOT):
    os.makedirs(NETWORK_ROOT)

class NetworkWars(QMainWindow):
    def __init__(self):
        super().__init__()
        self.vm_statuses = {}  # Dictionary to track VM statuses
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Network Wars")
        self.setGeometry(100, 100, 1200, 800)

        # Create the main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Network view
        self.network_view = QGraphicsView()
        self.network_scene = QGraphicsScene()
        self.network_view.setScene(self.network_scene)
        self.main_layout.addWidget(self.network_view, 2)

        # Side panel for bot management
        self.side_panel = QVBoxLayout()
        self.main_layout.addLayout(self.side_panel, 1)

        self.bot_list_label = QLabel("Bots")
        self.side_panel.addWidget(self.bot_list_label)

        self.bot_list = QListWidget()
        self.side_panel.addWidget(self.bot_list)

        self.create_bot_button = QPushButton("Create Bot")
        self.create_bot_button.clicked.connect(self.create_bot)
        self.side_panel.addWidget(self.create_bot_button)

        self.delete_bot_button = QPushButton("Delete Bot")
        self.delete_bot_button.clicked.connect(self.delete_bot)
        self.side_panel.addWidget(self.delete_bot_button)

        self.sandbox_button = QPushButton("Sandbox Mode")
        self.sandbox_button.clicked.connect(self.sandbox_mode)
        self.side_panel.addWidget(self.sandbox_button)

        self.competitive_button = QPushButton("Competitive Mode")
        self.competitive_button.clicked.connect(self.competitive_mode)
        self.side_panel.addWidget(self.competitive_button)

        # Console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setPlaceholderText("Console output will be here...")
        console_dock = QDockWidget("Console", self)
        console_dock.setWidget(self.console_output)
        console_dock.setFloating(False)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu("File")
        self.add_file_menu_actions(file_menu)

        # Create Edit menu
        edit_menu = menubar.addMenu("Edit")
        self.add_edit_menu_actions(edit_menu)

        # Create Help menu
        help_menu = menubar.addMenu("Help")
        self.add_help_menu_actions(help_menu)

        self.statusBar().showMessage('Ready')

        # Load existing bots
        self.load_bots()

        # Draw initial network map
        self.draw_network_map()

        # Timer to update network map
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_network_map)
        self.timer.start(5000)  # Update every 5 seconds

    def add_file_menu_actions(self, file_menu):
        create_bot_action = QAction("Create Bot", self)
        create_bot_action.triggered.connect(self.create_bot)
        file_menu.addAction(create_bot_action)

        list_bots_action = QAction("List Bots", self)
        list_bots_action.triggered.connect(self.list_bots)
        file_menu.addAction(list_bots_action)

        delete_bot_action = QAction("Delete Bot", self)
        delete_bot_action.triggered.connect(self.delete_bot)
        file_menu.addAction(delete_bot_action)

        file_menu.addSeparator()

        sandbox_action = QAction("Sandbox Mode", self)
        sandbox_action.triggered.connect(self.sandbox_mode)
        file_menu.addAction(sandbox_action)

        compete_action = QAction("Competitive Mode", self)
        compete_action.triggered.connect(self.competitive_mode)
        file_menu.addAction(compete_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def add_edit_menu_actions(self, edit_menu):
        edit_action = QAction("Edit Settings", self)
        edit_action.triggered.connect(self.edit_settings)
        edit_menu.addAction(edit_action)

    def add_help_menu_actions(self, help_menu):
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_bot(self):
        bot_name, ok = QInputDialog.getText(self, "Create Bot", "Enter bot name:")
        if ok and bot_name:
            bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}.py")
            if os.path.exists(bot_path):
                QMessageBox.warning(self, "Error", f"Bot {bot_name} already exists.")
            else:
                with open(bot_path, 'w') as bot_file:
                    bot_file.write("# AI Bot script\n")
                self.bot_list.addItem(bot_name)
                self.console_output.append(f"Bot {bot_name} created successfully.")
            self.statusBar().showMessage(f"Bot {bot_name} created.")

    def list_bots(self):
        self.bot_list.clear()
        bots = [f for f in os.listdir(NETWORK_ROOT) if f.endswith('.py')]
        self.bot_list.addItems(bots)
        self.console_output.append("Listed all bots.")
        self.statusBar().showMessage("Listed all bots.")

    def delete_bot(self):
        bot_name = self.bot_list.currentItem().text()
        if bot_name:
            bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}")
            if os.path.exists(bot_path):
                os.remove(bot_path)
                self.bot_list.takeItem(self.bot_list.currentRow())
                self.console_output.append(f"Bot {bot_name} deleted successfully.")
                self.statusBar().showMessage(f"Bot {bot_name} deleted.")
            else:
                QMessageBox.warning(self, "Error", f"Bot {bot_name} does not exist.")
        else:
            QMessageBox.warning(self, "Error", "No bot selected.")

    def sandbox_mode(self):
        bot_name = self.bot_list.currentItem().text()
        if bot_name:
            bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}")
            if os.path.exists(bot_path):
                try:
                    
                    result = subprocess.run([sys.executable, bot_path], capture_output=True, text=True)
                    self.console_output.append(f"Sandbox Mode Output for {bot_name}:\n{result.stdout}")

                    
                    vm_output = self.run_command_on_vm('vm_ip', 'username', 'password', 'ls')
                    self.console_output.append(f"VM Command Output:\n{vm_output}")

                    
                    self.update_vm_status('vm_ip', 'online')
                except Exception as e:
                    self.console_output.append(f"Error while running the bot {bot_name}:\n{e}")
                    self.update_vm_status('vm_ip', 'offline')
                self.statusBar().showMessage(f"Testing {bot_name} in sandbox mode.")
            else:
                QMessageBox.warning(self, "Error", f"Bot {bot_name} does not exist.")
        else:
            QMessageBox.warning(self, "Error", "No bot selected.")

    def competitive_mode(self):
        bot_name = self.bot_list.currentItem().text()
        if bot_name:
            bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}")
            if os.path.exists(bot_path):
                QMessageBox.information(self, "Competitive Mode", f"Entering {bot_name} into a tournament...")
                self.console_output.append(f"Entering {bot_name} into a tournament.")
                self.statusBar().showMessage(f"Entering {bot_name} into a tournament.")
                # Implement competitive mode logic here
            else:
                QMessageBox.warning(self, "Error", f"Bot {bot_name} does not exist.")
        else:
            QMessageBox.warning(self, "Error", "No bot selected.")

    def edit_settings(self):
        QMessageBox.information(self, "Edit Settings", "Edit settings clicked.")

    def show_about(self):
        QMessageBox.information(self, "About Network Wars", "Network Wars v1.0\nA game of AI bot competitions.")

    def load_bots(self):
        bots = [f for f in os.listdir(NETWORK_ROOT) if f.endswith('.py')]
        self.bot_list.addItems(bots)

    def draw_network_map(self):
        self.network_scene.clear()

        nodes = {
            'vm1': (0, 0, Qt.blue),
            'vm2': (200, 0, Qt.green),
            'vm3': (100, 100, Qt.red),
        }

        for vm, (x, y, color) in nodes.items():
            node = QGraphicsEllipseItem(QRectF(x, y, 50, 50))
            node.setBrush(QBrush(color))
            self.network_scene.addItem(node)

        
        self.network_scene.addLine(25, 25, 225, 25)
        self.network_scene.addLine(25, 25, 125, 125)
        self.network_scene.addLine(225, 25, 125, 125)

    def update_network_map(self):
        for vm_ip, status in self.vm_statuses.items():
            if status == 'online':
                color = Qt.green
            elif status == 'offline':
                color = Qt.red
            else:
                color = Qt.yellow

            
            self.update_vm_node(vm_ip, color)

    def update_vm_status(self, vm_ip, status):
        self.vm_statuses[vm_ip] = status
        self.console_output.append(f"Updated VM {vm_ip} status to {status}")

    def update_vm_node(self, vm_ip, color):
        
        for item in self.network_scene.items():
            if isinstance(item, QGraphicsEllipseItem):
                if item.rect().topLeft() == self.vm_status_to_position(vm_ip):
                    item.setBrush(QBrush(color))
                    break

    def vm_status_to_position(self, vm_ip):
        positions = {
            'vm1': (0, 0),
            'vm2': (200, 0),
            'vm3': (100, 100),
        }
        return positions.get(vm_ip, (0, 0))

    def run_command_on_vm(self, hostname, username, password, command):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            ssh.close()
            return output
        except Exception as e:
            return str(e)

def main():
    app = QApplication(sys.argv)
    ex = NetworkWars()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
