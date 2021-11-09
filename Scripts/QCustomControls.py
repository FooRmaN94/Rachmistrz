import sys
from PyQt5.QtWidgets import QLineEdit, QApplication
from PyQt5.QtGui import QDoubleValidator, QValidator
from PyQt5 import QtCore


#set validator to QLineEdit to collect only float data
class QDoubleBox(QLineEdit):
    def __init__(self):
        super().__init__()
        self.editingFinished.connect(self.validate)

    def validate(self):
        self.setText(self.text().replace(",", "."))
        validation_rule = QDoubleValidator(0, 1000000, 2)
        validation_rule.setLocale(QtCore.QLocale(1))
        validation_status = validation_rule.validate(self.text(), 1)

        print(validation_status)

        if validation_status[0] == QValidator.Acceptable:
            self.setFocus()
        else:
            self.setText("")

