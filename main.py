import sys
import pandas
from PyQt5.QtCore import(
    Qt
                           )
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QTableWidgetItem, QLabel, QVBoxLayout, QGridLayout, QTableWidget,
    QHBoxLayout, QFormLayout, QTabWidget, QDialog
)
from Scripts import Database as database
db = database.Database('database.db')

# class Dialog inherits from QDialog class
class Dialog(QDialog):
    def __init__(self, tab_id, edit, id, dialog_name="", parent=None):
        self.edit = edit
        self.id = id
        print("dialog name", dialog_name)
        super().__init__(parent)
        button_layout = QHBoxLayout()
        layout = QVBoxLayout()
        self.setWindowTitle(dialog_name)
        self.setLayout(layout)
        layout.addLayout(self.prepare_dialog(tab_id))
        button_layout.addWidget(QPushButton("Cancel",clicked= lambda: self.cancel_click()))
        layout.addLayout(button_layout)

    def person_click(self, fname, lname):
        if self.edit:
            db.edit_person(fname, lname,self.id)
        else:
            db.add_person(fname, lname)

    def prepare_dialog(self, tab_id):
        layout = QFormLayout()
        # Definitions of functions

        def person_dialog():
            fname = QLineEdit(self)
            lname = QLineEdit(self)
            if self.edit:
                fname.setText("Edited")
                lname.setText("Value")

            button = QPushButton("Ok", clicked=lambda:self.person_click(fname.text(), lname.text()))
            layout.addRow("Imię", fname)
            layout.addRow("Nazwisko", lname)
            layout.addRow(button)

            return layout
        # here we'll launch proper function on certain number
        switcher = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: person_dialog()
        }

        return switcher.get(tab_id, "error")

    def cancel_click(self):
        self.close()


class MainPage(QWidget):
    tab_names = ["Rekord", "Produkt", "Kategoria", "Podkategorie", "Tagi", "Wpływy", "Osoby"]
    tab = []

    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 600
        self.height = 233

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.init_tabs()
        self.widget()

    def person_button_press(self, edit, record_id=None):
        if (not edit) and not(record_id is None):
            db.remove_person(record_id)
        else:
            dlg = Dialog(6, edit, record_id)
            dlg.exec_()

# fun init tabs is getting info about tabs' names from tab_names variable, and it's adding it to the main window.

    def init_tabs(self):
        for i, text in enumerate(self.tab_names):
            self.tab.append(QWidget())
            self.tabs.addTab(self.tab[i], self.tab_names[i])

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        # Creating a tabs:
        self.layout.addWidget(self.tabs)
        self.create_tab_person()
        self.show()

    def create_tab_person(self):
        i = self.tab_names.index("Osoby")
        # Table with contents of person table
        table = create_table(db.get_person())
        button_add = QPushButton("Dodaj",clicked=lambda: self.person_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.person_button_press(True, 1))
        button_remove = QPushButton("Usuń", clicked=lambda: self.person_button_press(False, self.get_id(table)))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)

        table_row_height = 5
        table_columns_width = 4
        layout.addWidget(table, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)
        return

    def get_id(self, table):
        row = table.currentRow()
        item_id = table.item(table.currentRow(), 0)
        return item_id.data(Qt.DisplayRole.real)

def create_table(data):
    rows, columns = data.shape
    table = QTableWidget()
    table.setColumnCount(columns)
    table.setRowCount(rows)
    table.setHorizontalHeaderLabels(data.head())
    table.setColumnHidden(0, True)
    # fill data
    for i, r in enumerate(data.iterrows()):
        tmp = r[1].values
        for j, value in enumerate(tmp):
            if j == 0:
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, value)
                table.setItem(i, j, item)
            else:
                table.setItem(i, j, QTableWidgetItem(str(value)))

    return table


def main():
    app = QApplication(sys.argv)
    w = MainPage(title="RachMistrz")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
