import requests
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt, QSettings

API_URL = 'https://for-my-favourite-teacher.onrender.com/api/auth/register'

class QRegisterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings('MyCompany', 'MyApp')
        self.settings.setValue('auth/token', '') if not self.settings.value('auth/token') else ''

        main_layout = QGridLayout(self)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('Optional...')

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText('Required...')

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText('Required...')

        self.btn_reg = QPushButton('register')

        main_layout.addWidget(QLabel('Name:'), 0, 0)
        main_layout.addWidget(self.input_name, 0, 1)

        main_layout.addWidget(QLabel('Email:'), 1, 0)
        main_layout.addWidget(self.input_email, 1, 1)

        main_layout.addWidget(QLabel('Password:'), 2, 0)
        main_layout.addWidget(self.input_password, 2, 1)

        main_layout.addWidget(self.btn_reg, 3, 0, 1, 2)

        self.btn_reg.clicked.connect(self.register)

    def register(self):
        try:
            name = self.input_name.text().strip()
            email = self.input_email.text().strip()
            password = self.input_password.text().strip()

            if not email or not password:
                QMessageBox.information(self, 'Error', 'empty email or password')
                return

            response = requests.post(API_URL, json={'name': name, 'email': email, 'password': password})
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'You are registered!')
            info = response.json()

            self.settings.setValue('auth/token', info['accessToken'])

            self.clear_all()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_all(self):
        self.input_name.clear()
        self.input_email.clear()
        self.input_password.clear()