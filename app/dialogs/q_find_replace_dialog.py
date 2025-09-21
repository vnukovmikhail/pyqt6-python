from PyQt6.QtWidgets import (
    QTextEdit, QVBoxLayout,
    QDialog, QLineEdit, QPushButton, QHBoxLayout, QLabel, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextDocument, QTextCursor

class QFindReplaceDialog(QDialog):
    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.setWindowTitle('Find and Replace')
        self.text_edit = text_edit

        layout = QVBoxLayout(self)

        hl_find = QHBoxLayout()
        hl_find.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        hl_find.addWidget(self.find_input)
        layout.addLayout(hl_find)

        hl_replace = QHBoxLayout()
        hl_replace.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        hl_replace.addWidget(self.replace_input)
        layout.addLayout(hl_replace)

        self.case_checkbox = QCheckBox("Match case")
        layout.addWidget(self.case_checkbox)

        hl_buttons = QHBoxLayout()
        self.find_next_btn = QPushButton("Find Next")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")
        self.close_btn = QPushButton("Close")

        hl_buttons.addWidget(self.find_next_btn)
        hl_buttons.addWidget(self.replace_btn)
        hl_buttons.addWidget(self.replace_all_btn)
        hl_buttons.addWidget(self.close_btn)
        layout.addLayout(hl_buttons)

        self.find_next_btn.clicked.connect(self.find_next)
        self.replace_btn.clicked.connect(self.replace)
        self.replace_all_btn.clicked.connect(self.replace_all)
        self.close_btn.clicked.connect(self.close)

    def find_next(self):
        flags = QTextDocument.FindFlag(0)
        if self.case_checkbox.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively

        text = self.find_input.text()
        if not self.text_edit.find(text, flags):
            self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)
            self.text_edit.find(text, flags)

    def replace(self):
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == self.find_input.text():
            cursor.insertText(self.replace_input.text())
        self.find_next()

    def replace_all(self):
        text_to_find = self.find_input.text()
        replacement = self.replace_input.text()
        if not text_to_find:
            return

        flags = QTextDocument.FindFlag(0)
        if self.case_checkbox.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively

        self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)
        while self.text_edit.find(text_to_find, flags):
            cursor = self.text_edit.textCursor()
            cursor.insertText(replacement)
