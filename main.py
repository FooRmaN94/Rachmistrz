from Scripts import Database as database
db = database.Database('database.db')


import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton,QLabel,QVBoxLayout,QHBoxLayout, QFormLayout, QTabWidget,QDialog
)
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
        return
    def person_click(self, fname, lname):
        print("Twoja godnosc to", fname, lname)
        return
    def prepare_dialog(self, tab_id):
        layout = QFormLayout()
        #Definitions of functions
        def person_dialog():
            fname=QLineEdit(self)
            lname=QLineEdit(self)
            if (self.edit == True):
                fname.setText("Edited")
                lname.setText("Value")
            button = QPushButton("Ok",clicked=lambda:self.person_click(fname.text(),lname.text()))
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
        return
    def init_tabs(self):
        for i,text in enumerate(self.tab_names):
            self.tab.append(QWidget())
            self.tabs.addTab(self.tab[i],self.tab_names[i])

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        ## use above line or below
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        # Creating a tabs:
        self.layout.addWidget(self.tabs)
        self.create_tab_person()
        self.show()

    def create_tab_person(self):
        i = self.tab_names.index("Osoby")
        button_add = QPushButton("Dodaj",clicked = lambda: self.person_button_press(False))
        button_edit = QPushButton("Edytuj", clicked=lambda: self.person_button_press(True,1))
        button_remove = QPushButton("Usuń",clicked = lambda: self.person_button_press(False,1))
        layout = QFormLayout()
        self.tab[i].setLayout(layout)
        layout.addRow(button_add)
        layout.addRow(button_edit)
        layout.addRow(button_remove)
        return

def main():
    app = QApplication(sys.argv)
    w = MainPage(title="PyQt5")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
