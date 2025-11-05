import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTreeView, QPushButton, QWidget, \
    QLabel, QToolBar, QDialog, QLayout, QLineEdit, QDialogButtonBox
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
from database.db_code import add_folder, get_root_folders, get_other_folders, delete_folder, get_all_tabs, add_tab


class NewFolderDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new folder")
        self.setModal(True)


    #lay
        self.layout = QVBoxLayout()

    #title
        self.title = QLabel("Enter folder's name:")

    #line edit
        self.edit = QLineEdit()

    #buttons
        self.dialogButtons = QDialogButtonBox (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.dialogButtons.accepted.connect(self.acc)
        self.dialogButtons.rejected.connect(self.reject)


        self.layout.addWidget(self.title)
        self.layout.addWidget(self.edit)
        self.layout.addWidget(self.dialogButtons)
        self.setLayout(self.layout)

    def acc(self):
        self.setResult(QDialog.DialogCode.Accepted)
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    #NewFolderDialog
        self.nfd = NewFolderDialog()

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
    #delete_foldder_action
        delete_folder_action = QAction(QIcon(), "Delete folder", self)
        delete_folder_action.triggered.connect(self.drop_folder)
        toolbar.addAction(delete_folder_action)
    #model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name"])

    #data to model
        self.data_into_model()

    #creating a tree
        self.tree = QTreeView()
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
            item.setData(id_, Qt.ItemDataRole.UserRole)
            self.model.appendRow(item)
            id_to_item[id_] = item

        # other folders
        other_folders = get_other_folders()
        for folder in other_folders:
            id_, name, parent_id = folder
            item = QStandardItem(name)
            item.setEditable(True)
            item.setData(id_, Qt.ItemDataRole.UserRole)

            if parent_id in id_to_item:
                id_to_item[parent_id].appendRow(item)
            else:
                self.model.appendRow(item)

            id_to_item[id_] = item

        self.folders_id = id_to_item

        #self.tree.expandAll()
        self.folders_id = id_to_item
        print(self.folders_id)

    def add_folder(self):
        print("start")
        dialog = NewFolderDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_index = self.tree.selectedIndexes()

            if not selected_index:
                print("No folder selected — adding to root?")
                parent_id = None
            else:
                selected_item = self.model.itemFromIndex(selected_index[0])
                parent_id = selected_item.data(Qt.ItemDataRole.UserRole)

            folder_name = dialog.edit.text().strip()

            if not folder_name:
                print("Empty folder name!")
                return

            add_folder(folder_name, parent_id)

            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Name"])
            self.data_into_model()
            print("Folder added!")

        else:
            print("dialog closed")
        print("end")

    def drop_folder(self):
        selected_ind = self.tree.selectedIndexes()
        if selected_ind:
            selected_item = self.model.itemFromIndex(selected_ind[0])
            selected_id = selected_item.data(Qt.ItemDataRole.UserRole)
            delete_folder(selected_id)
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Name"])
            self.data_into_model()
        else:
            print("Nothing to delete!")



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()