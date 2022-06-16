from PyQt5 import QtWidgets
from PyQt5 import QtCore

class RefTablesViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("RefTablesViewer")

        self.HBoxLayout = QtWidgets.QHBoxLayout(self)
        self.HBoxLayout.setObjectName("HBoxLayout")

        self.setLayout(self.HBoxLayout)

    def add_to_HBoxLayout(self, ref_table):
        print("pozvan")
        self.HBoxLayout.addWidget(ref_table)

    def clear_HBoxLayout(self):
        table_count = self.HBoxLayout.count()
        if table_count == 0:
            return
        else:
            for i in range(table_count):
                print("indeks je: ", i)
                ref_table = self.HBoxLayout.itemAt(0).widget()
                self.HBoxLayout.removeWidget(ref_table)
                ref_table.deleteLater()