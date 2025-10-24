from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

from app.widgets.q_register_widget import QRegisterWidget
from app.widgets.q_login_widget import QLoginWidget

API_URL = 'https://for-my-favourite-teacher.onrender.com/api/auth'

class QAuthWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QRegisterWidget())
        layout.addWidget(QLoginWidget())
        layout.addStretch()