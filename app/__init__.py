import time
from PyQt6.QtWidgets import QMainWindow
from app.widgets.q_central_widget import QCentralWidget
from app.widgets.q_menu_bar_widget import QMenuBarWidget

APP_START_TIME = time.perf_counter()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt6 painter')
        self.setMinimumSize(500, 350)

        status = self.statusBar()
        elapsed = time.perf_counter() - APP_START_TIME
        status.showMessage(f'Program started in {elapsed:.3f} seconds', 3000)

        central_widget = QCentralWidget()
        self.setMenuBar(QMenuBarWidget(central_widget, status))
        self.setCentralWidget(central_widget)