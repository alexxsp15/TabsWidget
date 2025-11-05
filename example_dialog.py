# dialog_example.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel,
    QLineEdit, QDialogButtonBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class NameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введи своє ім'я")
        self.setModal(True)  # робить діалог модальним (блокує головне вікно)

        # Layout
        vbox = QVBoxLayout(self)

        # Підпис
        self.label = QLabel("Будь ласка, введи своє ім'я нижче:")
        vbox.addWidget(self.label)

        # Поле вводу
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Ваше ім'я...")
        vbox.addWidget(self.line_edit)

        # Кнопки OK / Cancel через QDialogButtonBox
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            orientation=Qt.Orientation.Horizontal,
            parent=self
        )
        vbox.addWidget(self.buttons)

        # Зв'язки
        self.buttons.accepted.connect(self.on_accept)   # натиснули OK
        self.buttons.rejected.connect(self.reject)      # натиснули Cancel

        # Додаткова кнопка, яка показує поточний текст (демо)
        show_btn = QPushButton("Показати (не закриває)")
        vbox.addWidget(show_btn)
        show_btn.clicked.connect(self.show_current_text)

    def on_accept(self):
        text = self.line_edit.text().strip()
        if not text:
            # Якщо порожнє, показати повідомлення та не закривати діалог
            QMessageBox.warning(self, "Увага", "Поле не може бути порожнім.")
            return
        # Якщо все гарно — встановити результат і закрити діалог як Accepted
        self.setResult(QDialog.DialogCode.Accepted)
        self.accept()

    def show_current_text(self):
        QMessageBox.information(self, "Поточний текст", f"В полі: «{self.line_edit.text()}»")


def main():
    app = QApplication(sys.argv)

    dlg = NameDialog()
    result = dlg.exec()  # запускаємо модально; поверне QDialog.DialogCode.Accepted або Rejected

    if result == QDialog.DialogCode.Accepted:
        name = dlg.line_edit.text().strip()
        print(f"Користувач ввів: {name}")
        # Можна показати ще головне вікно або повідомлення
        QMessageBox.information(None, "Привіт!", f"Привіт, {name}!")
    else:
        print("Діалог закрито / відхилено.")

    sys.exit(0)


if __name__ == "__main__":
    main()
