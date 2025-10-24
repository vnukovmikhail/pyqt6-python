import requests
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QGridLayout, QMessageBox, QSpinBox, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QSettings

from app.templates.q_region_template import QRegionTemplate

API_URL = 'https://for-my-favourite-teacher.onrender.com/api/regions'

class QRegionWidget(QWidget):
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

        id_label = QLabel('Id:')
        self.spin = QSpinBox()

        hl = QHBoxLayout()
        hl.addWidget(id_label)
        hl.addWidget(self.spin)
        hl.addStretch()

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('Input post name...')
        
        self.input_desc = QTextEdit()
        self.input_desc.setPlaceholderText('Input post description...')
        self.input_desc.setFixedHeight(60)
        

        self.btn_get = QPushButton('GET')
        self.btn_patch = QPushButton('PATCH')

        main_layout.addLayout(hl)
        main_layout.addWidget(self.input_name)
        main_layout.addWidget(self.input_desc)
        main_layout.addWidget(self.btn_get)
        main_layout.addWidget(self.btn_patch)
        main_layout.addWidget(scroll)

        self.btn_get.clicked.connect(self.get_post)
        self.btn_patch.clicked.connect(self.patch_post)

    def get_post(self):
        try:
            id = self.spin.value()

            response = requests.get(f'{API_URL}/{str(id)}')
            response.raise_for_status()
            post = response.json()

            print(post)
            
            self.clear_layout(self.content_layout)

            region = QRegionTemplate(post['id'], post['name'], post['description'], self.settings.value('auth/token'))
            region.removed.connect(self.get_post)
            self.content_layout.addWidget(region)

            self.content_layout.addStretch()

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def patch_post(self):
        id = self.spin.value()
        name = self.input_name.text().strip()
        desc = self.input_desc.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, 'Error', 'Input post name')
            return

        try:
            headers = {"Content-Type": "application/json"}
            headers["Authorization"] = f"Bearer {self.settings.value('auth/token')}"

            response = requests.patch(f'{API_URL}/{str(id)}', json={'name': name, 'description': desc}, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, 'Success', 'Post created!')

            self.input_name.clear()
            self.input_desc.clear()

            self.get_post()
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)