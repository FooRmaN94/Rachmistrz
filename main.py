import sys
import pandas
from Scripts.QCustomControls import QDoubleBox
from PyQt5 import(
    QtCore
)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QComboBox, QPushButton, QTableWidgetItem, QVBoxLayout, QGridLayout, QTableWidget,
    QFormLayout, QTabWidget, QDialog, QMessageBox, QDateEdit
)
from Scripts.Database import Database

db = Database('database.db')


# class Dialog inherits from QDialog class
class Dialog(QDialog):
    def __init__(self, tab_id, edit, id, dialog_name="", parent=None):
        self.edit = edit
        self.id = id
        super().__init__(parent)
        self.setWindowTitle(dialog_name)
        layout = QVBoxLayout()
        cancel_button = QPushButton("Cancel", clicked=lambda: self.cancel_click())
        dialog_layout = self.prepare_dialog(tab_id)()
        dialog_layout.addRow(cancel_button)
        layout.addLayout(dialog_layout)
        self.setLayout(layout)

    def person_click(self, fname, lname):
        if self.edit:
            show_message_box(db.edit_person(fname, lname, self.id))
            self.close()
        else:
            show_message_box(db.add_person(fname, lname))
            self.close()

    def category_click(self, category_name):
        if self.edit:
            show_message_box(db.edit_category(category_name, self.id))
            self.close()
        else:
            show_message_box(db.add_category(category_name))
            self.close()
    def sub_category_click(self, name, category_id):
        if self.edit:
            show_message_box(db.edit_sub_category(name, category_id, self.id))
            self.close()
        else:
            show_message_box(db.add_sub_category(name, category_id))
            self.close()

    def income_click(self, person_id, amount, date):
        if self.edit:
            show_message_box(db.edit_income(person_id, amount, date, self.id))
            self.close()
        else:
            show_message_box(db.add_income(person_id, amount, date))
            self.close()

    def prepare_dialog(self, tab_id):
        # Definitions of layout design functions

        def income_dialog():
            print("Income dialog is creating now...")
            layout = QFormLayout()
            person_id = QComboBox()
            people = db.get_person()
            person = []
            ids = []
            for unit in people.iterrows():
                person.append(''.join([unit[1].values[1], " ", unit[1].values[2]]))
                ids.append(unit[1].values[0])
            person_id.addItems(person)
            amount = QDoubleBox()
            date = QDateEdit(calendarPopup=True)
            if self.edit:
                data = db.get_income(self.id)
                record = data.iloc[0]
                person_id.setCurrentIndex(search_index(ids, record[1]))
                amount.setText(str(record[4]))
                date.setDate(QtCore.QDate.fromString(record[5], "dd.MM.yyyy"))
            else:
                date.setDate(QtCore.QDate.currentDate())
            button = QPushButton("Ok", clicked=lambda: self.income_click(ids[person_id.currentIndex()], amount.text(),
                                                                         date.text()))
            layout.addRow("Osoba", person_id)
            layout.addRow("Wpływ", amount)
            layout.addRow("Data", date)
            layout.addRow(button)
            return layout

        def category_dialog():
            print("category dialog is creating now...")
            layout = QFormLayout()
            category_name = QLineEdit()
            if self.edit:
                data = db.get_category(self.id)
                record = data.iloc[0]
                category_name.setText(record[1])
            button = QPushButton("Ok", clicked=lambda: self.category_click(category_name.text()))
            layout.addRow("Nazwa", category_name)
            layout.addRow(button)
            return layout


        def sub_category_dialog():
            print("sub_category dialog is creating now...")
            layout = QFormLayout()
            sub_category_name = QLineEdit()
            categories = db.get_category()
            category = []
            ids = []
            for unit in categories.iterrows():
                category.append(unit[1].values[1])
                ids.append(unit[1].values[0])
            category_id = QComboBox()
            category_id.addItems(category)
            if self.edit:
                data = db.get_sub_category(self.id)
                record = data.iloc[0]
                sub_category_name.setText(record[1])
                category_id.setCurrentIndex(search_index(ids, record[2]))
            button = QPushButton("Ok", clicked=lambda: self.sub_category_click(sub_category_name.text(),
                                                                               ids[category_id.currentIndex()]))
            layout.addRow("Nazwa podkategorii", sub_category_name)
            layout.addRow("Kategoria", category_id)
            layout.addRow(button)
            return layout

        def tag_dialog():
            print("tag dialog is creating now...")

        def product_dialog():
            print("product dialog is creating now...")

        def record_dialog():
            print("record dialog is creating now...")

        def person_dialog():
            print("person dialog is creating now...")
            layout = QFormLayout()
            fname = QLineEdit()
            lname = QLineEdit()
            if self.edit:
                data = db.get_person(self.id)
                record = data.iloc[0]
                fname.setText(record[1]) # take first_name from db and set as textbox text value
                lname.setText(record[2]) # take last_name from db and set as textbox text value
            button = QPushButton("Ok", clicked=lambda:self.person_click(fname.text(), lname.text()))
            layout.addRow("Imię", fname)
            layout.addRow("Nazwisko", lname)
            layout.addRow(button)
            print("person layout has ended returning now")
            return layout


        # here we'll launch proper function on certain number
        switcher = {
            0: record_dialog,
            1: product_dialog,
            2: category_dialog,
            3: sub_category_dialog,
            4: tag_dialog,
            5: income_dialog,
            6: person_dialog
        }

        return switcher.get(tab_id, "error")

    def cancel_click(self):
        self.close()


class MainPage(QWidget):
    tab_names = ["Rekord", "Produkt", "Kategorie", "Podkategorie", "Tagi", "Wpływy", "Osoby"]
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
        self.incomeTable = QTableWidget()
        self.tagTable = QTableWidget()
        self.categoryTable = QTableWidget()
        self.sub_categoryTable = QTableWidget()
        self.productTable = QTableWidget()
        self.recordTable = QTableWidget()
        # end of tables
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.init_tabs()
        self.widget()

    def button_pressed(self, edit, tab_name, tab_id, record_id=None):
        if record_id == -1:
            pass
        else:
            if not edit and not(record_id is None):
                test = db.remove(tab_id, record_id)
                show_message_box(test)
            else:
                dlg = Dialog(tab_id, edit, record_id, tab_name)
                dlg.exec_()
            table = self.get_table_data(tab_id)
            create_table(table['data'], table['table'])

    def get_table_data(self, tab_id):
        if tab_id == 0:
            return {'data': db.get_record(), 'table': self.recordTable}
        elif tab_id == 1:
            return {'data': db.get_product(), 'table': self.productTable}
        elif tab_id == 2:
            return {'data': db.get_category(), 'table': self.categoryTable}
        elif tab_id == 3:
            return {'data': db.get_sub_category(), 'table': self.sub_categoryTable}
        elif tab_id == 4:
            return {'data': db.get_tag(), 'table': self.tagTable}
        elif tab_id == 5:
            return {'data': db.get_income(), 'table': self.incomeTable}
        elif tab_id == 6:
            return {'data': db.get_person(), 'table': self.personTable}
    # fun init tabs is getting info about tabs' names from tab_names variable, and it's adding it to the main window.

    def init_tabs(self):
        for i, text in enumerate(self.tab_names):
            self.tab.append(QWidget())
            self.tabs.addTab(self.tab[i], self.tab_names[i])

    def table_selection_changed(self):
        print("wybrano komórki")

    def tab_changed(self, tab_id):
        if self.tab[tab_id].layout():
            table = self.get_table_data(tab_id)
            create_table(table['data'], table['table'])
        else:
            self.create_tab_layout(tab_id)

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        # Creating a tabs:
        self.layout.addWidget(self.tabs)
       # self.create_tab_layout(0)
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.tabs.blockSignals(False)
        self.show()

    def create_tab_layout(self, index):
        table = self.get_table_data(index)
        create_table(table['data'], table['table'])
        button_add = QPushButton("Dodaj", clicked=lambda: self.button_pressed(False, self.tab_names[index], index))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.button_pressed(True, self.tab_names[index], index,
                                    self.get_id(table['table'])))
        button_remove = QPushButton("Usuń", clicked=lambda: self.button_pressed(False, self.tab_names[index], index,
                                        self.get_id(table['table'])))
        layout = QGridLayout()
        self.tab[index].setLayout(layout)
        #if any data is selected, then function "table_selection_changed' will be exectuted
        #table['table'].blockSignals(True)
        #table['table'].itemSelectionChanged.connect(self.table_selection_changed())
        #table['table'].blockSignals(False)
        table_row_height = 5
        table_columns_width = 4
        layout.addWidget(table['table'], 0, 0, table_row_height, table_columns_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_columns_width - 1, 1, 1)

    def get_id(self, table):
        # pick currently selected row, and point to it's first hidden column which contains the ID and return it as ID
        row = table.currentRow()
        print("selected indexes number:",len(table.selectedIndexes()))
        print("selected row",row)
        if row == -1:
            return row
        else:
            item_id = table.item(table.currentRow(), 0)
            return item_id.data(QtCore.Qt.DisplayRole.real)


def show_message_box(test):
    alert = QMessageBox()
    print("type", type(test[0]))
    if test[0]:
        alert.setWindowTitle("Sukces")
        alert.setIcon(QMessageBox.Information)
        alert.setText("Pomyślnie wykonano operację")
        alert.setStandardButtons(QMessageBox.Ok)
    else:
        alert.setWindowTitle("Błąd")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Błąd w trakcie wykonywania operacji.")
        alert.setInformativeText(str(test[1]))
        alert.setStandardButtons(QMessageBox.Ok)
    alert.exec_()

def search_index(list, searched_value):
        for i, item in enumerate(list):
            if item == searched_value:
                return i

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
    db.create_database()
    w = MainPage(title="RachMistrz")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
