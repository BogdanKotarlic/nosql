from PyQt5 import QtCore, QtGui, QtWidgets

from main_window_model import MainWindowModel
from utils.mysql_utils import MySQLUtils
from data_handler_dialog.data_handler_dialog import DataHandlerDialog

class MainWindowController:
    def __init__(self):
        self.main_window_model = MainWindowModel()
        self.mySQL_utils = MySQLUtils()
        self.data_handler_viewer = None
    
    def load_and_connect_db(self, databasesTableWidget, databasesComboBox, statusBar):
        self.main_window_model.load_and_connect_db(databasesTableWidget, databasesComboBox, statusBar)
    
    def create_database(self, new_database_name, statusBar, databasesComboBox, databasesTableWidget):
        self.main_window_model.create_database(new_database_name, statusBar, databasesComboBox, databasesTableWidget)

    def delete_selected_database(self, databasesTableWidget, databasesComboBox, statusBar):
        self.main_window_model.delete_selected_database(databasesTableWidget, databasesComboBox, statusBar)
    
    def load_collections(self, current_database_name, collectionsComboBox):
        if current_database_name:
            if current_database_name != "none":
                self.main_window_model.load_collections(current_database_name, collectionsComboBox)

    def load_table_data(self, current_collection_name, databaseDataTableWidget):
        if current_collection_name != "":
            self.main_window_model.load_table_data(current_collection_name, databaseDataTableWidget)

    def delete_row(self, databaseDataTableWidget, database_name, collection_name):
        self.main_window_model.delete_row(databaseDataTableWidget, database_name, collection_name)

    def show_data_handler_dialog(self, current_database_name, current_table_name, mode, databaseDataTableWidget, statusBar):
        if mode == "insert":
            dlg = DataHandlerDialog(current_database_name, current_table_name, None, mode, statusBar)
            dlg.exec()
            self.load_table_data(current_table_name, databaseDataTableWidget)
        elif mode == "update":
            data = [record for record in self.mySQL_utils.get_table_data(current_table_name)]
            selected_indexes = databaseDataTableWidget.selectedIndexes()
            for s in selected_indexes:
                dlg = DataHandlerDialog(current_database_name, current_table_name, data[s.row()], mode, statusBar)
                dlg.exec()
            self.load_table_data(current_table_name, databaseDataTableWidget)
        elif mode == "search":
            dlg = DataHandlerDialog(current_database_name, current_table_name, None, mode, statusBar)
            closed = dlg.exec()
            if not closed:
                self.main_window_model.load_table_data(current_table_name, databaseDataTableWidget, dlg.get_search_results())
        
