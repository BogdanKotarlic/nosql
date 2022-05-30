from PyQt5 import QtWidgets


def show(title, message):
    message_box = QtWidgets.QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.exec()
