from PyQt6.QtWidgets import QTabWidget, QLabel, QStatusBar

from app.widgets.q_regions_widget import QRegionsWidget
from app.widgets.q_region_widget import QRegionWidget
from app.widgets.q_auth_widget import QAuthWidget

class QCentralWidget(QTabWidget):
    def __init__(self, status: QStatusBar):
        super().__init__()

        self.addTab(QAuthWidget(), 'auth')
        self.addTab(QRegionsWidget(), 'regions')
        self.addTab(QRegionWidget(), 'region[solo]')