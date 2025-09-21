from PyQt6.QtWidgets import QMenuBar, QStatusBar

from app.dialogs.q_file_menu import QFileMenu

from app.widgets.q_central_widget import QCentralWidget

class QMenuBarWidget(QMenuBar):
    def __init__(self, tab_widget:QCentralWidget=None, status_bar:QStatusBar=None):
        super().__init__()
        
        self.addMenu(QFileMenu(self, tab_widget, status_bar))
        

        