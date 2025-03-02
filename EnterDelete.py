import sys
import os
import winshell
from win32com.client import Dispatch
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QClipboard


class TextProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text Editor')
        self.setGeometry(100, 100, 800, 600)

        # Верхнее текстовое поле
        self.upper_text = QTextEdit(self)
        # Нижнее текстовое поле (только для чтения)
        self.lower_text = QTextEdit(self)
        self.lower_text.setReadOnly(True)

        # Зеленая кнопка
        self.green_btn = QPushButton('Удалить enters', self)
        self.green_btn.setStyleSheet("background-color: green")
        self.green_btn.clicked.connect(self.process_text)

        # Фиолетовая кнопка
        self.purple_btn = QPushButton('Копировать в буфер', self)
        self.purple_btn.setStyleSheet("background-color: purple")
        self.purple_btn.clicked.connect(self.copy_to_clipboard)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.upper_text)
        layout.addWidget(self.green_btn)
        layout.addWidget(self.lower_text)
        layout.addWidget(self.purple_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def process_text(self):
        text = self.upper_text.toPlainText()
        processed_text = text.replace('\n', '').replace('\r', '')
        self.lower_text.setPlainText(processed_text)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.lower_text.toPlainText())


def create_shortcut():
    desktop_path = winshell.desktop()
    shortcut_path = os.path.join(desktop_path, "Удалить Enter.lnk")

    target_path = os.path.abspath(__file__)  # Путь к текущему скрипту
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.save()


if __name__ == "__main__":
    create_shortcut()  # Создаем ярлык при запуске <button class="citation-flag" data-index="7">
    app = QApplication(sys.argv)
    window = TextProcessor()
    window.show()
    sys.exit(app.exec())