from PyQt5.QtWidgets import QLabel,QApplication

class gui():
    app=QApplication([])
    def __init__(self):

        label = QLabel("Hello world")
        label.show()
        return
    def show(self):
        print("Trying to show exec")
        self.app.exec_()
        print("Theorecitaly after launch")
        return