import sys
import pandas
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QTableWidget, QHBoxLayout, QFormLayout, QTabWidget,QDialog
)
from Scripts import Database as database
db = database.Database('database.db')

# class Dialog inherits from QDialog class
class Dialog(QDialog):
    def __init__(self, tab_id, edit, id, dialog_name="", parent=None):
        self.edit=edit
        self.id=id
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
            fname=QLineEdit(self)
            lname=QLineEdit(self)
            if self.edit:
                fname.setText("Edited")
                lname.setText("Value")

            button = QPushButton("Ok", clicked=lambda:self.person_click(fname.text(), lname.text()))
            layout.addRow("Imie",fname)
            layout.addRow("Nazwisko",lname)
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

        return switcher.get(tab_id,"error")
    def cancel_click(self):
        self.close()

class MainPage(QWidget):
    tab_names = ["Rekord","Produkt","Kategoria","Podkategorie","Tagi","Wpływy","Osoby"]
    tab=[]
    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 800
        self.height = 500

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.init_tabs()
        self.widget()

    def person_button_press(self,edit,id=None):
        if (not edit and not id==None):
            print("remove code here")
        else:
            dlg=Dialog(6,edit,id)
            dlg.exec_()
        
		# fun init tabs is getting info about tabs' names from tab_names variable, and it's adding it to the main window.
		
    def init_tabs(self):
        for i,text in enumerate(self.tab_names):
            self.tab.append(QWidget())
            self.tabs.addTab(self.tab[i],self.tab_names[i])

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
		table=create_table(db.get_person())
        button_add = QPushButton("Dodaj",clicked = lambda: self.person_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.person_button_press(True,1))
        button_remove = QPushButton("Usuń",clicked = lambda: self.person_button_press(False,1))
        layout = QGridLayout()
        self.tab[i].setLayout(layout)
		
		# table_row_height = 5
		# table_colums_width = 4
		layout.addWidget(table,0,0,table_row_height,table_colums_width)
        layout.addWidget(button_add, table_row_height, 0, 1, 1)
        layout.addWidget(button_edit, table_row_height, 1, 1, 1)
        layout.addWidget(button_remove, table_row_height, table_colums_width - 1, 1, 1)
        return

def create_table(data):

	table = QTableWidget()
	return table

def main():
    app = QApplication(sys.argv)
    w = MainPage(title="PyQt5")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
