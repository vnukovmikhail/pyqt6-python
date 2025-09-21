from PyQt6.QtWidgets import QTabWidget, QApplication, QLabel, QStatusBar
from app.widgets.q_edit_widget import QEditWidget

class QCentralWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        # self.create_tab(QEditWidget('fit.txt'), 'no faf')

    def create_tab(self, editwidget: QEditWidget, name):
        self.addTab(editwidget, name)
        self.setCurrentIndex(self.count() - 1)

    def close_tab(self, index):
        self.removeTab(index)
        # if self.count() <= 0:
        #     QApplication.quit()

    def ii(self):
        print(self.indexOf(self))