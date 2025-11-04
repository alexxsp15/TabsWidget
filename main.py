import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTreeView, QPushButton, QWidget, QLabel, QToolBar
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
from database.db_code import add_folder, get_root_folders, get_other_folders

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    #main widget
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()

    #tool bar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

    #addfolder_action
        addfolder_action = QAction(QIcon(), "Add folder", self)
        addfolder_action.triggered.connect(self.add_folder)
        toolbar.addAction(addfolder_action)
    #model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name"])

    #data to model
        self.data_into_model()

    #creating a tree
        self.tree = QTreeView()
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)
        self.tree.setModel(self.model)


    #mainLayout
        self.mainLayout.addWidget(self.tree)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)


        self.folders_id = {}
    def data_into_model(self):
        id_to_item = {}

    # root folders
        root_folders = get_root_folders()
        for folder in root_folders:
            id_, name = folder[0], folder[1]
            item = QStandardItem(name)
            item.setEditable(True)
            self.model.appendRow(item)
            id_to_item[id_] = item

    # other folders
        other_folders = get_other_folders()
        for folder in other_folders:
            id_, name, parent_id = folder
            item = QStandardItem(name)
            item.setEditable(True)

            if parent_id in id_to_item:
                id_to_item[parent_id].appendRow(item)
            else:
                self.model.appendRow(item)

            id_to_item[id_] = item

        self.folders_id = id_to_item
        print(self.folders_id)


    def add_folder(self):
        print("start")
        selected_index = self.tree.selectedIndexes()
        selected_id = None
        if not selected_index:
            print("nah")
        else:
            selected_folder = self.model.itemFromIndex(selected_index[0])
            print("stuck here")
            for id, item in self.folders_id.items():
                if selected_folder == item:
                    print(id)
                    add_folder("new_one", id)
                    self.tree.update()
                    print("slay!")
                else: print("nah2")
        print("end")




app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()