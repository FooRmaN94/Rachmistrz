# from Scripts import Database as database
# from Scripts import GUI
# db = database.Database('database.db')


import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QFrame, QHBoxLayout, QVBoxLayout, QFormLayout, QTabWidget
)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QRect


class MainPage(QWidget):
    tab_names = ["Rekord","Produkt","Kategoria","Podkategorie","Tagi","Wpływy","Osoby"]
    tab=[]
    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        print(self.tab_names)
        self.personLastName = QLineEdit()
        self.personFirstName = QLineEdit()
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 800
        self.height = 500
        self.init_tabs()
        self.widget()
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
        self.create_tab_osoby()
        self.layout.addWidget(self.tabs)
        self.show()

    def create_tab_osobyey(self):
        i = self.tab_names.index("Osoby")
        layout = QFormLayout()
        self.tab[i].setLayout(layout)
        return

    def create_tab_osoby(self):
        i = self.tab_names.index("Osoby")
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        #form_layout.addRow()
        layout.addWidget(form_layout)
        self.tab[i].setLayout(layout)
        return


def main():
    app = QApplication(sys.argv)
    w = MainPage(title="PyQt5")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
