import os, shutil
from PyQt6.QtWidgets import QMenu, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSettings

from app.gui.widgets.q_central_widget import QCentralWidget

from app.gui.dialogs.export_dialog import ExportDialog
from app.gui.dialogs.import_dialog import ImportDialog

def pack(folder: str, archive_name: str, format_: str = "zip"):
    folder = os.path.abspath(folder)
    archive_file = shutil.make_archive(archive_name, format_, root_dir=folder)
    return archive_file

class QFileMenu(QMenu):
    def __init__(self, parent=None, tab_widget:QCentralWidget = None):
        super().__init__('File', parent)

        self.settings = QSettings('config.ini', QSettings.Format.IniFormat)

        self.addSeparator()

        export_action = QAction('Export', self)
        export_action.triggered.connect(self.open_export_dialog)
        self.addAction(export_action)

        import_action = QAction('Import', self)
        import_action.triggered.connect(self.open_import_dialog)
        self.addAction(import_action)

    def open_export_dialog(self):
        # folder = QFileDialog.getExistingDirectory(self, 'Choose folder to archivate')
        # if not folder:
        #     return

        folder = self.settings.value('User/Folder')

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save archive',
            'archive.zip',
            "Zip archive (*.zip);;Tar.gz archive (*.tar.gz)"
        )

        if not save_path:
            return

        if save_path.endswith(".tar.gz"):
            fmt = "gztar"
        elif save_path.endswith(".zip"):
            fmt = "zip"
        else:
            fmt = "zip"

        try:
            archive = pack(folder, os.path.splitext(save_path)[0], fmt)
            QMessageBox.information(self, 'Done', f'✅ Archive was created:\n{archive}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'❌ Failed to pack: {e}')

        # dialog = ExportDialog(self)
        # if dialog.exec():
        #     print("Экспорт выполнен ✅")
        # else:
        #     print("Экспорт отменён ❌")

    def open_import_dialog(self):
        dialog = ImportDialog(self)
        if dialog.exec():
            print("Импорт выполнен ✅")
        else:
            print("Импорт отменён ❌")