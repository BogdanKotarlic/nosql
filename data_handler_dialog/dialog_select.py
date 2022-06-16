from PyQt5 import QtWidgets, QtCore
from utils.mysql_utils import MySQLUtils
from data_handler_dialog import message_box
from data_handler_dialog.table_reference_spec import load_spec


class DialogSelect(QtWidgets.QDialog):
    def __init__(self, db_name, table_name, column):
        super().__init__()

        self.setObjectName("DialogSelect")
        self.resize(400, 400)
        self.column = column
        self.selected = None
        mysql_spec = load_spec()
        self.id_column_name = None
        if table_name in mysql_spec.keys():
            self.id_column_name = mysql_spec[table_name]["id_col"]

        self.setWindowTitle("Dialog")

        self.mySQL_utils = MySQLUtils()

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.layout = QtWidgets.QVBoxLayout()

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.tableWidget.setSortingEnabled(True)

        self.layout.addWidget(self.tableWidget)

        self.button = QtWidgets.QPushButton(self)
        self.button.setObjectName("button")
        self.button.setText("Select")

        self.button.clicked.connect(self.select)

        self.layout.addWidget(self.button)

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
            for column_index, column in enumerate(self.columns):
                self.tableWidget.setItem(
                    row, column_index, QtWidgets.QTableWidgetItem((str(self.data[row][column_index]))))

        if self.id_column_name != "":
            self.tableWidget.setColumnHidden(0, True)

    def select(self):
        selected_indexes = self.tableWidget.selectedIndexes()
        selected_index = selected_indexes[0]
        # print(self.columns, self.column)
        self.selected = self.data[selected_index.row()][self.columns.index(self.column)]
        self.close()
    
    def get_selected(self):
        return self.selected