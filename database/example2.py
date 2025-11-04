import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLabel, QMessageBox
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Приклад QToolBar")

        # Головний текст у центрі
        self.label = QLabel("Натисни кнопку в ToolBar", alignment=Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)

        # === Створення ToolBar ===
        toolbar = QToolBar("Головна панель інструментів")
        toolbar.setMovable(True)  # Дозволити перетягування
        self.addToolBar(toolbar)

        # --- Дія 1 ---
        action_hello = QAction(QIcon(), "Привіт", self)
        action_hello.setStatusTip("Показати повідомлення 'Привіт'")
        action_hello.triggered.connect(self.say_hello)
        toolbar.addAction(action_hello)

        # --- Дія 2 ---
        action_clear = QAction(QIcon(), "Очистити", self)
        action_clear.setStatusTip("Очистити текст")
        action_clear.triggered.connect(self.clear_label)
        toolbar.addAction(action_clear)

        # --- Розділювач ---
        toolbar.addSeparator()

        # --- Дія Вихід ---
        action_exit = QAction("Вихід", self)
        action_exit.setStatusTip("Закрити програму")
        action_exit.triggered.connect(self.close)
        toolbar.addAction(action_exit)

        # Вмикаємо підказки в статус-барі
        self.statusBar()

    def say_hello(self):
        self.label.setText("Привіт!")
        QMessageBox.information(self, "Hello", "Ви натиснули кнопку 'Привіт'")

    def clear_label(self):
        self.label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
