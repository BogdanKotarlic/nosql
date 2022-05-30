from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from utils.mysql_utils import MySQLUtils

class MainWindowModel:
    def __init__(self):
        self.mySQL_utils = MySQLUtils()
    
    def load_and_connect_db(self, databasesTableWidget, databasesComboBox, statusBar):
        self.mySQL_utils.load_and_connect_db(statusBar)
        # databases tab
        self.fill_database_table(databasesTableWidget)
        # data tab
        databases_typle = self.mySQL_utils.get_all_databases()
        databasesComboBox.clear()
        databasesComboBox.addItem("none")
        databasesComboBox.addItems([database_name[0] for database_name in databases_typle])

    def create_database(self, new_database_name, statusBar, databasesComboBox, databasesTableWidget):
        if databasesComboBox.findText(new_database_name) != -1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Database with that name already exists.")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

        elif (self.mySQL_utils.check_connection() and new_database_name != ""):
            self.mySQL_utils.create_database(new_database_name, statusBar)
            databasesComboBox.addItem(new_database_name)
            print(new_database_name, "dodao")
            self.fill_database_table(databasesTableWidget)

    def delete_selected_database(self, databasesTableWidget, databasesComboBox, statusBar):
        selected_indexes = databasesTableWidget.selectedIndexes()
        for s in selected_indexes:
            database_name = databasesTableWidget.itemFromIndex(s).text()
            dropped = self.mySQL_utils.delete_database(database_name, statusBar)
            if (dropped):
                databasesTableWidget.removeRow(s.row())
                index = databasesComboBox.findText(database_name)
                databasesComboBox.removeItem(index)
        

    def load_collections(self, current_database_name, collectionsComboBox):
        table_names_typle = self.mySQL_utils.get_all_tables(current_database_name)
        collectionsComboBox.clear()
        collectionsComboBox.addItems([table_name[0] for table_name in table_names_typle])

    def load_table_data(self, current_collection_name, databaseDataTableWidget, table_data=None):
        if table_data == None:
            table_data = self.mySQL_utils.get_table_data(current_collection_name)

        table_row_count = len(table_data)

        table_columns = self.mySQL_utils.get_table_columns(current_collection_name)
        # print(table_columns) // [('id', b'int', 'NO', 'PRI', None, 'auto_increment'), ('naziv', b'varchar(45)', 'YES', '', None, '')]
        table_column_names = [table_name[0] for table_name in table_columns]
        table_column_count = len(table_column_names)

        databaseDataTableWidget.setRowCount(table_row_count)
        databaseDataTableWidget.setColumnCount(table_column_count)
        databaseDataTableWidget.setHorizontalHeaderLabels(table_column_names)

        for row in range(table_row_count):
            for column in range(table_column_count):
                databaseDataTableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(table_data[row][column])))

    def delete_row(self, databaseDataTableWidget, database_name, collection_name):
        row_index = databaseDataTableWidget.currentRow()
        row_data_id = databaseDataTableWidget.item(row_index, 0).text()
        delete_done = self.mySQL_utils.delete_row(database_name, collection_name, row_data_id)
        if delete_done:
            self.load_table_data(collection_name, databaseDataTableWidget)
    
    def fill_database_table(self, databasesTableWidget):
        columns = ["Database Name"]
        databases_typle = self.mySQL_utils.get_all_databases()
        num_rows = len(databases_typle)
        num_cols = len(columns)

        databasesTableWidget.setRowCount(num_rows)

        databasesTableWidget.setColumnCount(num_cols)

        databasesTableWidget.setHorizontalHeaderLabels(columns)

        for row in range(num_rows):
            for column in range(num_cols):
                databasesTableWidget.setItem(
                    row, column, QtWidgets.QTableWidgetItem((str(databases_typle[row][column]))))