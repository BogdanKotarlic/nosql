from PyQt5 import QtWidgets
from utils.mysql_utils import MySQLUtils
from data_handler_dialog import message_box


class DialogSelect(QtWidgets.QDialog):
    def __init__(self, db_name, table_name, column):
        super().__init__()

        self.column = column

        self.selected = None

        self.setWindowTitle("Dialog")

        self.mySQL_utils = MySQLUtils()

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.layout = QtWidgets.QVBoxLayout()

        self.button = QtWidgets.QPushButton(self)
        self.button.setObjectName("button")
        self.button.setText("Select")

        self.button.clicked.connect(self.select)

        self.layout.addWidget(self.button)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.tableWidget.setSortingEnabled(True)

        self.layout.addWidget(self.tableWidget)

        # self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)



        self.data = self.mySQL_utils.get_table_data(db_name, table_name)
        self.columns = [column[0]
                   for column in self.mySQL_utils.get_table_columns(db_name, table_name)]
        num_rows = len(self.data)
        if num_rows > 0:
            num_cols = len(self.data[0])
        else:
            num_cols = 0
            # self.statusMessage.setText("No Data")
            message_box.show("Notification", "No Data!")
            return

        self.tableWidget.setRowCount(num_rows)

        self.tableWidget.setColumnCount(num_cols)

        self.tableWidget.setHorizontalHeaderLabels(self.columns)

        for row in range(num_rows):
            for column in range(num_cols):
                self.tableWidget.setItem(
                    row, column, QtWidgets.QTableWidgetItem((str(self.data[row][column]))))

    def select(self):
        selected_indexes = self.tableWidget.selectedIndexes()
        selected_index = selected_indexes[0]
        # print(self.columns, self.column)
        self.selected = self.data[selected_index.row()][self.columns.index(self.column)]
        self.close()
    
    def get_selected(self):
        return self.selected