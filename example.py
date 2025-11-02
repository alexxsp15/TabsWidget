import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTreeView, QVBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class VirtualFileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Віртуальна файлова система (QTreeView + QStandardItemModel)")
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        # Створюємо модель
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Назва", "Тип"])

        # Наповнюємо даними
        self.populate_virtual_data()

        # Створюємо дерево
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.expandAll()  # розкрити всі папки
        self.tree.setHeaderHidden(False)
        layout.addWidget(self.tree)

    def populate_virtual_data(self):
        """Створюємо віртуальні папки і файли"""
        # Коренева "папка"
        root = QStandardItem("Local Disk (C:)")
        root.setEditable(False)
        self.model.appendRow([root, QStandardItem("Диск")])

        # Папка games
        games = QStandardItem("games")
        games.setEditable(False)
        root.appendRow([games, QStandardItem("Папка")])

        # Вкладені папки
        folder_444 = QStandardItem("444")
        folder_777 = QStandardItem("777")
        games.appendRow([folder_444, QStandardItem("Папка")])
        games.appendRow([folder_777, QStandardItem("Папка")])

        # Інші папки на "диску"
        photoshop = QStandardItem("Adobe Photoshop")
        epic = QStandardItem("Epic Games")
        fallguys = QStandardItem("FallGuys")
        root.appendRow([photoshop, QStandardItem("Папка")])
        root.appendRow([epic, QStandardItem("Папка")])
        root.appendRow([fallguys, QStandardItem("Папка")])

        # Додамо кілька "файлів" у FallGuys
        fallguys.appendRow([QStandardItem("readme.txt"), QStandardItem("Файл")])
        fallguys.appendRow([QStandardItem("config.ini"), QStandardItem("Файл")])
        fallguys.appendRow([QStandardItem("save1.dat"), QStandardItem("Файл")])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = VirtualFileBrowser()
    viewer.show()
    sys.exit(app.exec())
