from PyQt5 import QtCore, QtGui, QtWidgets

from mySQL_tab_component.mySQL_tab_model import MySQLTabModel
from utils.mysql_utils import MySQLUtils
from data_handler_dialog.data_handler_dialog import DataHandlerDialog

class MySQLTabController:
    def __init__(self):
        self.mySQL_tab_model = MySQLTabModel()
        self.mySQL_utils = MySQLUtils()
    
    def load_table_data(self, database_name, table_name, dataTableWidget):
        self.mySQL_tab_model.load_table_data(database_name, table_name, dataTableWidget)

    def delete_row(self, database_name, table_name, dataTableWidget):
        row_index = dataTableWidget.currentRow()
        row_data_id = dataTableWidget.item(row_index, 0).text()
        delete_done = self.mySQL_utils.delete_row(database_name, table_name, row_data_id)
        if delete_done:
            self.load_table_data(database_name, table_name, dataTableWidget)

    def show_data_handler_dialog(self, database_name, table_name, mode, dataTableWidget, statusBar):
        if mode == "insert":
            dlg = DataHandlerDialog(database_name, table_name, None, mode, statusBar)
            dlg.exec()
            self.load_table_data(database_name, table_name, dataTableWidget)
        elif mode == "update":
            data = [record for record in self.mySQL_utils.get_table_data(database_name, table_name)]
            selected_indexes = dataTableWidget.selectedIndexes()
            for s in selected_indexes:
                dlg = DataHandlerDialog(database_name, table_name, data[s.row()], mode, statusBar)
                dlg.exec()
            self.load_table_data(database_name, table_name, dataTableWidget)
        elif mode == "search":
            dlg = DataHandlerDialog(database_name, table_name, None, mode, statusBar)
            closed = dlg.exec()
            if not closed:
                self.mySQL_tab_model.load_table_data(database_name, table_name, dataTableWidget, dlg.get_search_results())