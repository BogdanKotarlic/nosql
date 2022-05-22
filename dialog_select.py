from PyQt5 import QtCore, QtGui, QtWidgets
import mysql_functions
from functools import partial
import spec

class DialogSelect(QtWidgets.QDialog):
    def __init__(self, db_name, table_name, column):
        super().__init__()


        self.column = column
        self.selected = None

        self.setWindowTitle("Dialog")

        self.layout = QtWidgets.QVBoxLayout()

        self.button = QtWidgets.QPushButton(self)
        self.button.setObjectName("selectButton")
        self.button.setText("Select")
        self.button.clicked.connect(self.select)

        self.layout.addWidget(self.button)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.tableWidget.setSortingEnabled(True)

        self.layout.addWidget(self.tableWidget)

        self.setLayout(self.layout)


        data = mysql_functions.show_table(db_name, table_name)
        self.data = data
        columns = [column[0] for column in mysql_functions.show_columns(db_name, table_name)]
        self.columns = columns

        num_rows = len(data)
        num_cols = len(columns)

        self.tableWidget.setRowCount(num_rows)
        self.tableWidget.setColumnCount(num_cols)

        self.tableWidget.setHorizontalHeaderLabels(columns)

        for row in range(num_rows):
            for column in range(num_cols):
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem((str(data[row][column]))))

    def select(self):
        selected_indexes = self.tableWidget.selectedIndexes()
        selected_index = selected_indexes[0]
        self.selected = self.data[selected_index.row()][self.columns.index(self.column)]

        self.close()

    def get_selected(self):
        return self.selected