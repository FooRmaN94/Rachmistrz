import sys
import pandas
from PyQt5 import(
    QtCore
)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QComboBox, QPushButton, QTableWidgetItem, QVBoxLayout, QGridLayout, QTableWidget,
    QFormLayout, QTabWidget, QDialog, QMessageBox, QDateEdit
)
from Scripts import Database as database
db = database.Database('database.db')


# class Dialog inherits from QDialog class
class Dialog(QDialog):
    def __init__(self, tab_id, edit, id, dialog_name="", parent=None):
        self.edit = edit
        self.id = id
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setWindowTitle(dialog_name)
        self.setLayout(layout)
        layout.addLayout(self.prepare_dialog(tab_id))
        layout.addWidget(QPushButton("Cancel", clicked=lambda: self.cancel_click()))

    def __del__(self):
        print("destroyed")

    def person_click(self, fname, lname):
        if self.edit:
            show_message_box(db.edit_person(fname, lname,self.id))
            self.close()
        else:
            show_message_box(db.add_person(fname, lname))
            self.close()

    def income_click(self):
        print("Hello from income")

    def prepare_dialog(self, tab_id):
        # Definitions of layout design functions

        def income_dialog():
            print("Income dialog is creating now...")
            layout = QFormLayout(self)
            person_id = QComboBox(self)
            amount = QLineEdit(self)
            date = QDateEdit(calendarPopup=True)
            #if self.edit:
                #data = db.get_income(self.id)
                #record = data.iloc[0]
            button = QPushButton("Ok", clicked=lambda: self.income_click())
            layout.addRow("Osoba", person_id)
            layout.addRow("Nazwisko", amount)
            layout.addRow("Data", date)
            layout.addRow(button)
            return layout

        def person_dialog():
            print("person dialog is creating now...")
            layout = QFormLayout(self)
            fname = QLineEdit(self)
            lname = QLineEdit(self)
            if self.edit:
                data = db.get_person(self.id)
                record = data.iloc[0]
                fname.setText(record[1]) # take first_name from db and set as textbox text value
                lname.setText(record[2]) # take last_name from db and set as textbox text value

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
            5: income_dialog(),
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
        # init tables
        self.personTable = QTableWidget()
        self.incomeTable = QTabWidget()
        # end of tables
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.init_tabs()
        self.widget()

    def person_button_press(self, edit, record_id=None):
        # if remove was clicked
        if not edit and not(record_id is None):
            test = db.remove_person(record_id)
            show_message_box(test)
        # Else dialog will edit or add. Function below will handle it
        else:
            dlg = Dialog(6, edit, record_id, "Osoba")
            dlg.exec_()
        # Refresh the table
        create_table(db.get_person(), self.personTable)

    def income_button_press(self, edit, record_id=None):
        # if remove was clicked
        if (not edit) and not(record_id is None):
            test = db.remove_income(record_id)
            show_message_box(test)
        # Else dialog will edit or add. Function below will handle it
        else:
            dlg = Dialog(5, edit, record_id)
            dlg.exec_()
        # Refresh the table
        #create_table(db.get_income(), self.incomeTable)

    # fun init tabs is getting info about tabs' names from tab_names variable, and it's adding it to the main window.

    def init_tabs(self):
        for i, text in enumerate(self.tab_names):
            self.tab.append(QWidget())
            self.tabs.addTab(self.tab[i], self.tab_names[i])

    def tab_changed(self, i):
        if self.tab[i].layout():
            pass
        elif i == 0:
            self.create_tab_record()
        elif i == 1:
            self.create_tab_product()
        elif i == 2:
            self.create_tab_category()
        elif i == 3:
            self.create_tab_subcategory()
        elif i == 4:
            self.create_tab_tag()
        elif i == 5:
            self.create_tab_income()
        elif i == 6:
            self.create_tab_person()

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        # Creating a tabs:
        self.layout.addWidget(self.tabs)
        self.create_tab_record()
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.tabs.blockSignals(False)
        self.show()

    def create_tab_person(self):
        i = self.tab_names.index("Osoby")
        # Table with contents of person table
        create_table(db.get_person(), self.personTable)
        button_add = QPushButton("Dodaj",clicked=lambda: self.person_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.person_button_press(True, self.get_id(self.personTable)))
        button_remove = QPushButton("Usuń", clicked=lambda: self.person_button_press(False, self.get_id(self.personTable)))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
        table_row_height = 5
        table_columns_width = 4
        layout.addWidget(self.personTable, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)
        return

    def create_tab_income(self):
        i = self.tab_names.index("Wpływy")
        button_add = QPushButton("Dodaj",clicked=lambda: self.income_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.income_button_press(True, 0))
        button_remove = QPushButton("Usuń", clicked=lambda: self.income_button_press(False, 0))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
        table_row_height = 5
        table_columns_width = 4
        #layout.addWidget(self.personTable, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)

    def create_tab_tag(self):
        i = self.tab_names.index("Tagi")
        button_add = QPushButton("Dodaj",clicked=lambda: self.tag_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.tag_button_press(True, 0))
        button_remove = QPushButton("Usuń", clicked=lambda: self.tag_button_press(False, 0))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
        table_row_height = 5
        table_columns_width = 4
        #layout.addWidget(self.personTable, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)

    def create_tab_subcategory(self):
        i = self.tab_names.index("Podkategorie")
        button_add = QPushButton("Dodaj",clicked=lambda: self.subcategory_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.subcategory_button_press(True, 0))
        button_remove = QPushButton("Usuń", clicked=lambda: self.subcategory_button_press(False, 0))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
        table_row_height = 5
        table_columns_width = 4
        #layout.addWidget(self.personTable, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)

    def create_tab_category(self):
        i = self.tab_names.index("Kategorie")
        button_add = QPushButton("Dodaj",clicked=lambda: self.category_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.category_button_press(True, 0))
        button_remove = QPushButton("Usuń", clicked=lambda: self.category_button_press(False, 0))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
        table_row_height = 5
        table_columns_width = 4
        #layout.addWidget(self.personTable, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)

    def create_tab_product(self):
        i = self.tab_names.index("Produkt")
        button_add = QPushButton("Dodaj", clicked=lambda: self.product_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.product_button_press(True, 0))
        button_remove = QPushButton("Usuń", clicked=lambda: self.product_button_press(False, 0))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
        table_row_height = 5
        table_columns_width = 4
        #layout.addWidget(self.personTable, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)

    def create_tab_record(self):
        i = self.tab_names.index("Rekord")
        button_add = QPushButton("Dodaj",clicked=lambda: self.record_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.record_button_press(True, 0))
        button_remove = QPushButton("Usuń", clicked=lambda: self.record_button_press(False, 0))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
        table_row_height = 5
        table_columns_width = 4
        #layout.addWidget(self.personTable, 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)

    def get_id(self, table):
        # pick currently selected row, and point to it's first hidden column which contains the ID and return it as ID
        item_id = table.item(table.currentRow(), 0)
        return item_id.data(QtCore.Qt.DisplayRole.real)


def show_message_box(test):
    alert = QMessageBox()
    if test:
        alert.setWindowTitle("Sukces")
        alert.setIcon(QMessageBox.Information)
        alert.setText("Pomyślnie wykonano operację")
        alert.setStandardButtons(QMessageBox.Ok)
    else:
        alert.setWindowTitle("Błąd")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Błąd w trakcie wykonywania operacji")
        alert.setStandardButtons(QMessageBox.Ok)
    alert.exec_()


def create_table(data, table):
    rows, columns = data.shape
    table.setColumnCount(columns)
    table.setRowCount(rows)
    table.setHorizontalHeaderLabels(data.head())
    table.setColumnHidden(0, True)
    table.horizontalHeader().setStretchLastSection(True)
    # fill data
    for i, r in enumerate(data.iterrows()):
        tmp = r[1].values
        for j, value in enumerate(tmp):
            if j == 0:
                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, value)
                table.setItem(i, j, item)
            else:
                table.setItem(i, j, QTableWidgetItem(str(value)))


def main():
    app = QApplication(sys.argv)
    w = MainPage(title="RachMistrz")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
