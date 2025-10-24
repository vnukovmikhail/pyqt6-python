import requests
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QMessageBox, QStyle
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QPixmap, QFont
from io import BytesIO

API_URL = 'https://for-my-favourite-teacher.onrender.com/api/auth/login'

class QLoginWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings('MyCompany', 'MyApp')
        self.settings.setValue('auth/token', '') if not self.settings.value('auth/token') else ''

        main_layout = QGridLayout(self)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText('Required...')

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText('Required...')

        self.btn_log = QPushButton('login')
        self.btn_out = QPushButton('logout')

        self.label_status = QLabel('Unauthorized')
        self.label_status.setFont(QFont('monospace', 15, 700, False))
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setStyleSheet('color: red;') 

        main_layout.addWidget(QLabel('Email:'), 0, 0)
        main_layout.addWidget(self.input_email, 0, 1)

        main_layout.addWidget(QLabel('Password:'), 1, 0)
        main_layout.addWidget(self.input_password, 1, 1)

        main_layout.addWidget(self.btn_log, 2, 0, 1, 2)
        main_layout.addWidget(self.btn_out, 3, 0, 1, 2)
        main_layout.addWidget(self.label_status, 4, 0, 1, 2)

        self.btn_log.clicked.connect(self.login)
        self.btn_out.clicked.connect(self.logout)

        self.label_status.setText('Authorized') if self.settings.value('auth/token') else ''
        self.label_status.setStyleSheet('color: green;') if self.settings.value('auth/token') else ''

    def login(self):
        try:
            email = self.input_email.text().strip()
            password = self.input_password.text().strip()

            if not email or not password:
                QMessageBox.information(self, 'Error', 'empty email or password')
                return

            response = requests.post(API_URL, json={'email': email, 'password': password})
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'You are authorized!')
            info = response.json()

            print(info)

            self.settings.setValue('auth/token', info['accessToken'])

            self.label_status.setText('Authorized')
            self.label_status.setStyleSheet('color: green;') 

            self.clear_all()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def logout(self):
        try:
            self.settings.setValue('auth/token', '') if self.settings.value('auth/token') else ''
            self.label_status.setText('Unauthorized')
            self.label_status.setStyleSheet('color: red;') 
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_all(self):
        self.input_email.clear()
        self.input_password.clear()