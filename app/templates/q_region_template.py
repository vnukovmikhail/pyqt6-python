import requests
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QMessageBox, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

API_URL = "https://for-my-favourite-teacher.onrender.com/api/regions"

class QRegionTemplate(QWidget):
    removed = pyqtSignal()
    def __init__(self, id: int, name: str, description: str, cities: list[str] = [], key: str = ''):
        super().__init__()

        self.id = id
        self.token = key

        # self.setStyleSheet('border: 1px solid green;')

        layout = QGridLayout(self)

        line = QLabel(f'Id: {str(self.id)} | Name: `{name}`')
        desc = QLabel(f'Info: `{description}`') if description else ''
        btn = QPushButton('^ remove ^')
        btn.setFont(QFont('monospace', 7))
        btn.setFixedHeight(15)

        layout.addWidget(line, 0, 0)
        layout.addWidget(desc, 1, 0) if description else ''
        layout.addWidget(btn, 2, 0)

        btn.clicked.connect(self.remove_data)

    def remove_data(self):
        try:
            headers = {"Content-Type": "application/json"}
            headers["Authorization"] = f"Bearer {self.token}"
            response = requests.delete(f'{API_URL}/{self.id}', headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'Post deleted!')

            self.removed.emit()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
