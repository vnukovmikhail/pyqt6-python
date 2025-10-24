import requests
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QMessageBox, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QSettings

from app.templates.q_region_template import QRegionTemplate

API_URL = "https://for-my-favourite-teacher.onrender.com/api/regions"

class QRegionsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings('MyCompany', 'MyApp')
        self.settings.setValue('auth/token', '') if not self.settings.value('auth/token') else ''

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('Input post name...')
        
        self.input_desc = QTextEdit()
        self.input_desc.setPlaceholderText('Input post description...')
        self.input_desc.setFixedHeight(60)
        

        self.btn_get = QPushButton('GET')
        self.btn_post = QPushButton('POST')

        main_layout.addWidget(self.input_name)
        main_layout.addWidget(self.input_desc)
        main_layout.addWidget(self.btn_get)
        main_layout.addWidget(self.btn_post)

        self.btn_get.clicked.connect(self.get_posts)
        self.btn_post.clicked.connect(self.create_post)

        self.get_posts()

    def showEvent(self, a0):
        self.get_posts()
        return super().showEvent(a0)

    def get_posts(self):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            posts = response.json()
            
            self.clear_layout(self.content_layout)
            for post in posts:
                region = QRegionTemplate(post['id'], post['name'], post['description'], post['cities'], self.settings.value('auth/token'))
                region.removed.connect(self.get_posts)
                self.content_layout.addWidget(region)
            self.content_layout.addStretch()

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def create_post(self):
        name = self.input_name.text().strip()
        desc = self.input_desc.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, 'Error', 'Input post name')
            return

        try:
            response = requests.post(API_URL, json={'name': name, 'description': desc})
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'Post created!')

            self.input_name.clear()
            self.input_desc.clear()

            self.get_posts()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)