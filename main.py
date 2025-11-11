import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTreeView, QPushButton, QWidget, \
    QLabel, QToolBar, QDialog, QLayout, QLineEdit, QDialogButtonBox, QTabWidget
from PyQt6.QtCore import Qt, QModelIndex, QSize
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QAction, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
from database.db_code import add_folder, get_root_folders, get_other_folders, delete_folder, get_all_tabs, add_tab, get_tab_by_id


def load_stylesheet(filename):
    """Завантажує QSS файл з папки styles"""

    base_dir = os.path.dirname(__file__)
    style_path = os.path.join(base_dir, "styles", filename)
    with open(style_path, "r", encoding="utf-8") as f:
        return f.read()


class MyTabs(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setMovable(True)
        self.setMinimumSize(QSize(500, 600))

    #adding tab
    def add_tab(self, id_):
        tab = get_tab_by_id(id_)

        tab = tab[0]

        tab_id = tab[0]
        name = tab[1]
        link = tab[2]

        widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel(name)
        link_label = QLabel(link)

        layout.addWidget(title_label)
        layout.addWidget(link_label)

        widget.setLayout(layout)

        self.addTab(widget, name)

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

class NeWTabDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add new tab")
        self.setModal(True)

    #lay
        self.lay = QVBoxLayout()

    #title
        self.title_name = QLabel("Enter tab's name:")

    #line
        self.line_name = QLineEdit()

    # title
        self.title_link = QLabel("Enter tab's link:")

    # line
        self.line_link = QLineEdit()

    #buttons
        self.dialogButtons = QDialogButtonBox (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.dialogButtons.accepted.connect(self.acc)
        self.dialogButtons.rejected.connect(self.reject)

        self.lay.addWidget(self.title_name)
        self.lay.addWidget(self.line_name)
        self.lay.addWidget(self.title_link)
        self.lay.addWidget(self.line_link)
        self.lay.addWidget(self.dialogButtons)
        self.setLayout(self.lay)

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
        self.mainWidget.setStyleSheet("background-color: #0D0D0D;")
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
    #add_tab_action
        add_tab_action = QAction(QIcon(), "Add tab", self)
        add_tab_action.triggered.connect(self.plus_tab)
        toolbar.addAction(add_tab_action)
    #model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name"])

    #data to model
        self.data_into_model()

    #creating a tree
        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.setModel(self.model)
        self.tree.selectionModel().selectionChanged.connect(self.show_tab)
        self.tree.setStyleSheet(load_stylesheet("tree.qss"))

    # tabWidget
        self.tabs = MyTabs()

    #mainLayout
        self.mainLayout.addWidget(self.tree)
        self.mainLayout.addWidget(self.tabs)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)


        self.folders_id = {}
        self.tabs_id = {}

    def data_into_model(self):
        id_to_item = {}

        # root folders
        root_folders = get_root_folders()
        for folder in root_folders:
            id_, name = folder[0], folder[1]
            item = QStandardItem(name)
            item.setEditable(True)
            item.setData(id_, Qt.ItemDataRole.UserRole)
            item.setData("folder", Qt.ItemDataRole.UserRole + 1)
            self.model.appendRow(item)
            id_to_item[id_] = item

        # other folders
        other_folders = get_other_folders()
        for folder in other_folders:
            id_, name, parent_id = folder
            item = QStandardItem(name)
            item.setEditable(True)
            item.setData(id_, Qt.ItemDataRole.UserRole)
            item.setData("folder", Qt.ItemDataRole.UserRole + 1)

            if parent_id in id_to_item:
                id_to_item[parent_id].appendRow(item)
            else:
                self.model.appendRow(item)

            id_to_item[id_] = item

        #now tabs
        tabs = get_all_tabs()
        id_to_tab = {}
        for tab in tabs:
            id_ = tab[0]
            name = tab[1]
            parent_id = tab[7]
            item = QStandardItem(name)
            item.setEditable(True)
            item.setData(id_, Qt.ItemDataRole.UserRole)
            item.setData("tab", Qt.ItemDataRole.UserRole + 1)

            if parent_id in id_to_item:
                id_to_item[parent_id].appendRow(item)
            else:
                self.model.appendRow(item)

            id_to_tab[id_] = item

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

    def plus_tab(self):
        print("start!")
        dialog = NeWTabDialog()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = self.tree.selectedIndexes()

            if not selected:
                print("nothing selected!")
                return
            else:
                selection = self.model.itemFromIndex(selected[0])
                folder_id = selection.data(Qt.ItemDataRole.UserRole)

            tab_name = dialog.line_name.text().strip()
            tab_link = dialog.line_link.text().strip()

            if not tab_name or not tab_link:
                print("no data!")
                return

            add_tab(tab_name, tab_link, folder_id)
            self.model.clear()
            self.model.setHorizontalHeaderLabels(["Name"])
            self.data_into_model()
            print("tab's added!")
        else:
            print("dialog closed")
        print("end")

    def show_tab(self):
        index = self.tree.selectedIndexes()[0]
        item = self.model.itemFromIndex(index)
        id_ = item.data(Qt.ItemDataRole.UserRole)
        item_type = item.data(Qt.ItemDataRole.UserRole + 1)

        if item_type == "tab":
            self.tabs.add_tab(id_)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()