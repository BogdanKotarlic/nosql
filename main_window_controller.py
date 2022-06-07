from PyQt5 import QtCore, QtGui, QtWidgets

from main_window_model import MainWindowModel
from utils.mysql_utils import MySQLUtils
from data_handler_dialog.data_handler_dialog import DataHandlerDialog

class MainWindowController:
    def __init__(self):
        self.main_window_model = MainWindowModel()
        self.mySQL_utils = MySQLUtils()
        self.data_handler_viewer = None
    

    def load_and_connect_mysql_db(self, mySQLTreeWidget, statusBar):
        self.main_window_model.load_and_connect_mysql_db(mySQLTreeWidget, statusBar)
    
    def create_mysql_database(self, newMySQLNameLineEdit, mySQLTreeWidget, statusBar):
        new_database_name = newMySQLNameLineEdit.text()
        newMySQLNameLineEdit.clear()
        self.main_window_model.create_mysql_database(new_database_name, mySQLTreeWidget, statusBar)

    def delete_selected_mysql_database(self, mySQLTreeWidget, statusBar):
        self.main_window_model.delete_selected_mysql_database(mySQLTreeWidget, statusBar)
    
    # def load_collections(self, current_database_name, collectionsComboBox):
    #     if current_database_name:
    #         if current_database_name != "none":
    #             self.main_window_model.load_collections(current_database_name, collectionsComboBox)

    # def delete_row(self, databaseDataTableWidget, database_name, collection_name):
    #     self.main_window_model.delete_row(databaseDataTableWidget, database_name, collection_name)
 
    def add_mysql_table_tab(self, treeItem, column, dataTabWidget, statusBar):
        table_name = treeItem.text(column)
        # provera da li je kliknuta tabela ili baza
        if treeItem.parent() != None:
            database_name = treeItem.parent().text(column)
            self.main_window_model.add_mysql_table_tab(database_name, table_name, dataTabWidget, statusBar)

    def close_tab(self, tab_index, dataTabWidget):
        dataTabWidget.removeTab(tab_index)

    #Mongo
    def load_and_connect_mongodb(self, mongoDBTreeWidget, statusBar):
        self.main_window_model.load_and_connect_mongodb(mongoDBTreeWidget, statusBar)
    
    def delete_selected_mongodb(self, mongoDBTreeWidget, statusBar):
        self.main_window_model.delete_selected_mongodb(mongoDBTreeWidget, statusBar)