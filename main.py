from Scripts import Database as database
from PyQt5.QtWidgets import QApplication,QLabel

db = database.Database('database.db')
app = QApplication([])
label = QLabel("Hello world")
label.show()
app.exec_()



#db.create_database()

