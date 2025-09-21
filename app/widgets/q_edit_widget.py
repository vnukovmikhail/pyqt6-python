from PyQt6.QtWidgets import QTextEdit, QWidget, QHBoxLayout, QColorDialog, QInputDialog, QFontDialog, QFileDialog, QStatusBar
from PyQt6.QtGui import QAction, QKeySequence, QFont, QTextCharFormat
from PyQt6.QtCore import Qt

from app.dialogs.q_find_replace_dialog import QFindReplaceDialog

class QEditWidget(QWidget):
    def __init__(self, PATH_TO_FILE: str = '', status_bar: QStatusBar = None):
        super().__init__()
        self.PATH_TO_FILE = PATH_TO_FILE
        self.STATUS_BAR = status_bar

        content = ''
        if PATH_TO_FILE:
            try:
                with open(PATH_TO_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                content = f'Something going wrong: {PATH_TO_FILE} - not found'

        self.text_edit = QTextEdit()
        self.text_edit.installEventFilter(self)

        if content:
            if PATH_TO_FILE.endswith('.html'):
                self.text_edit.setHtml(content)
            elif PATH_TO_FILE.endswith('.txt'):
                self.text_edit.setPlainText(content)


        self.text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.show_context_menu)

        self.underline_action = QAction('Underline', self)
        self.underline_action.setShortcut(QKeySequence.StandardKey.Underline)
        self.underline_action.setShortcutVisibleInContextMenu(True)
        self.underline_action.triggered.connect(self.underline_text)

        self.bold_action = QAction('Bold', self)
        self.bold_action.setShortcut(QKeySequence.StandardKey.Bold)
        self.bold_action.setShortcutVisibleInContextMenu(True)
        self.bold_action.triggered.connect(self.bold_text)

        self.italic_action = QAction('Italic', self)
        self.italic_action.setShortcut(QKeySequence.StandardKey.Italic)
        self.italic_action.setShortcutVisibleInContextMenu(True)
        self.italic_action.triggered.connect(self.italic_text)

        self.color_action = QAction('Color', self)
        self.color_action.setShortcut(QKeySequence.StandardKey.Close)
        self.color_action.setShortcutVisibleInContextMenu(True)
        self.color_action.triggered.connect(self.change_color)

        self.resize_action = QAction('Resize', self)
        self.resize_action.setShortcut(QKeySequence.StandardKey.Refresh)
        self.resize_action.setShortcutVisibleInContextMenu(True)
        self.resize_action.triggered.connect(self.change_font_size)

        self.font_action = QAction('Font', self)
        self.font_action.setShortcut(QKeySequence.StandardKey.Forward)
        self.font_action.setShortcutVisibleInContextMenu(True)
        self.font_action.triggered.connect(self.change_font_family)

        self.save_action = QAction('Save', self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.setShortcutVisibleInContextMenu(True)
        self.save_action.triggered.connect(self.save_text)

        self.find_action = QAction('Find', self)
        self.find_action.setShortcut(QKeySequence.StandardKey.Find)
        self.find_action.setShortcutVisibleInContextMenu(True)
        self.find_action.triggered.connect(self.show_find_replace)

        self.text_edit.addAction(self.underline_action)
        self.text_edit.addAction(self.bold_action)
        self.text_edit.addAction(self.italic_action)
        self.text_edit.addAction(self.color_action)
        self.text_edit.addAction(self.resize_action)
        self.text_edit.addAction(self.font_action)
        self.text_edit.addAction(self.save_action)
        self.text_edit.addAction(self.find_action)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.text_edit)

    def show_context_menu(self, pos):
        menu = self.text_edit.createStandardContextMenu()
        menu.addSeparator()

        menu.addAction(self.underline_action)
        menu.addAction(self.bold_action)
        menu.addAction(self.italic_action)
        menu.addAction(self.color_action)
        menu.addAction(self.resize_action)
        menu.addAction(self.font_action)

        menu.addSeparator()

        menu.addAction(self.save_action)

        menu.addSeparator()

        menu.addAction(self.find_action)

        menu.exec(self.text_edit.mapToGlobal(pos))

    
    def eventFilter(self, obj, event):
        if obj is self.text_edit and event.type() == event.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Return, Qt.Key.Key_Enter):
                cursor = self.text_edit.textCursor()
                if event.key() == Qt.Key.Key_Space:
                    cursor.insertText(" ")
                else:
                    cursor.insertBlock()

                fmt = QTextCharFormat()
                cursor.setCharFormat(fmt)
                self.text_edit.setTextCursor(cursor)
                return True
        return super().eventFilter(obj, event)

    def underline_text(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()

        cursor.setPosition(start)
        while cursor.position() < end:
            cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
            char_fmt = cursor.charFormat()
            char_fmt.setFontUnderline(not char_fmt.fontUnderline())
            cursor.mergeCharFormat(char_fmt)

        cursor.endEditBlock()

    def bold_text(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()

        cursor.setPosition(start)
        while cursor.position() < end:
            cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
            char_fmt = cursor.charFormat()
            char_fmt.setFontWeight(QFont.Weight.Bold if char_fmt.fontWeight() != QFont.Weight.Bold  else QFont.Weight.Normal)
            cursor.mergeCharFormat(char_fmt)

        cursor.endEditBlock()

    def italic_text(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()

        cursor.setPosition(start)
        while cursor.position() < end:
            cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
            char_fmt = cursor.charFormat()
            char_fmt.setFontItalic(not char_fmt.fontItalic())
            cursor.mergeCharFormat(char_fmt)

        cursor.endEditBlock()

    def change_color(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        color = QColorDialog.getColor()
        if not color.isValid():
            return

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()
        cursor.setPosition(start)

        while cursor.position() < end:
            cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
            char_fmt = cursor.charFormat()
            char_fmt.setForeground(color)
            cursor.mergeCharFormat(char_fmt)

        cursor.endEditBlock()

    def change_font_size(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        size, ok = QInputDialog.getDouble(self, 'Font size', 'Choose font size:', 12, 1, 100, 1)
        if not ok:
            return

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()
        cursor.setPosition(start)

        while cursor.position() < end:
            cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
            char_fmt = cursor.charFormat()
            char_fmt.setFontPointSize(size)
            cursor.mergeCharFormat(char_fmt)

        cursor.endEditBlock()

    def change_font_family(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        font, ok = QFontDialog.getFont(self.text_edit.font(), self, "Выберите шрифт")
        if not ok:
            return

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()
        cursor.setPosition(start)

        while cursor.position() < end:
            cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
            char_fmt = cursor.charFormat()
            char_fmt.setFontFamily(font.family()) 
            char_fmt.setFontPointSize(font.pointSizeF())
            cursor.mergeCharFormat(char_fmt)

        cursor.endEditBlock()

    def save_text(self):
        if not self.PATH_TO_FILE:
            file_path, selected_filter = QFileDialog.getSaveFileName(self, 'Save file', '', "HTML Files (*.html);;Text Files (*.txt)")
            if not file_path:
                return
            
            if selected_filter.startswith('HTML') and not file_path.endswith('.html'):
                file_path += '.html'
            elif selected_filter.startswith('Text') and not file_path.endswith('.txt'):
                file_path += '.txt'

            if file_path.endswith('.txt'):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toHtml())
        else:
            if self.PATH_TO_FILE.endswith('.txt'):
                with open(self.PATH_TO_FILE, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
            else:
                with open(self.PATH_TO_FILE, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toHtml())

        self.STATUS_BAR.showMessage('Successfully saved!', 3000)

    def show_find_replace(self):
        dialog = QFindReplaceDialog(self.text_edit)
        dialog.exec()