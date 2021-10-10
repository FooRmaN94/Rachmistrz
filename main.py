# from Scripts import Database as database
# from Scripts import GUI
# db = database.Database('database.db')


import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton,QLabel,QVBoxLayout,QHBoxLayout, QFormLayout, QTabWidget,QDialog
)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QRect
class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        button_layout=QHBoxLayout()
        layout = QVBoxLayout()
        self.setWindowTitle("Your Dialog")
        self.setLayout(layout)
        button_layout.addWidget(QPushButton("Ok",clicked= lambda: self.dialogClick()))
        button_layout.addWidget(QPushButton("Cancel",clicked= lambda: self.dialogClick()))
        layout.addWidget(QLabel("testowo"))
        layout.addLayout(button_layout)
        return
    def dialogClick(self):
        self.close()

class MainPage(QWidget):
    tab_names = ["Rekord","Produkt","Kategoria","Podkategorie","Tagi","Wpływy","Osoby"]
    tab=[]
    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        print(self.tab_names)
        self.personLastName = QLineEdit(self)
        self.personFirstName = QLineEdit(self)
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 800
        self.height = 500
        self.init_tabs()
        self.widget()

    def osoby_button_press(self):
        dlg=Dialog(self)
        dlg.exec_()
        return
    def init_tabs(self):
        for i,text in enumerate(self.tab_names):
            self.tab.append(QWidget())
            self.tabs.addTab(self.tab[i],self.tab_names[i])

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        ## use above line or below
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        # Creating a tabs:
        self.layout.addWidget(self.tabs)
        self.create_tab_osoby()
        self.show()

    def create_tab_osoby(self):
        i = self.tab_names.index("Osoby")
        layout = QFormLayout()
        self.tab[i].setLayout(layout)
       # layout.addRow("Imie", self.personFirstName)
       # layout.addRow("Nazwisko", self.personLastName)
        layout.addRow(QPushButton("Add",clicked = lambda: self.osoby_button_press()))
        return

def main():
    app = QApplication(sys.argv)
    w = MainPage(title="PyQt5")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
