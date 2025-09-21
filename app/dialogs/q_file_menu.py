import os
from PyQt6.QtWidgets import QMenu, QFileDialog, QStatusBar
from PyQt6.QtGui import QAction

from app.widgets.q_central_widget import QCentralWidget
from app.widgets.q_edit_widget import QEditWidget

class QFileMenu(QMenu):
    def __init__(self, parent=None, tab_widget:QCentralWidget=None, status_bar:QStatusBar=None):
        super().__init__('File', parent)
        self.tabs = tab_widget
        self.sb = status_bar

        self.addSeparator()

        export_action = QAction('New', self)
        export_action.triggered.connect(lambda: self.tabs.create_tab(QEditWidget('', status_bar=self.sb), '[new file]'))
        self.addAction(export_action)

        import_action = QAction('Open', self)
        import_action.triggered.connect(self.open_import_dialog)
        self.addAction(import_action)

    def open_import_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "HTML Files (*.html);;Text Files (*.txt)")
        if not file_path:
            return
        file_name = os.path.basename(file_path)
        self.tabs.create_tab(QEditWidget(file_path, self.sb), file_name)