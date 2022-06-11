from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
from PyQt5.QtCore import Qt

from utils.mongo_utils import MongoUtils

class MongoTabModel: 
    def __init__(self):
        self.mongo_utils = MongoUtils()

    def load_table_data(self, database_name, table_name, dataTableWidget, table_data=None):
        if table_data == None:
            table_data = self.mongo_utils.get_table_data(database_name)
        
        #table_row_count = len(table_data)

        #table_columns = self.mongo_utils.get_table_columns(database_name, table_name)

        #table_column_names = [table_name[0] for table_name in table_columns]
        #table_column_count = len(table_column_names)

        #dataTableWidget.setRowCount(table_row_count)
        #dataTableWidget.setColumnCount(table_column_count)
        #dataTableWidget.setHorizontalHeaderLabels(table_column_names)

        #for row in range(table_row_count):
            #for column in range(table_column_count):
                #dataTableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(table_data[row][column])))