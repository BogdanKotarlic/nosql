from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem
from PyQt5.QtCore import Qt
from mongoDB_component.mongoDB_viewer import MongoTabViewer

from utils.mysql_utils import MySQLUtils
from mySQL_tab_component.mySQL_tab_viewer import MySQLTabViewer
from utils.mongo_utils import MongoUtils

class MainWindowModel:
    def __init__(self):
        self.mySQL_utils = MySQLUtils()
        self.mongo_utils = MongoUtils()
    
    def load_and_connect_mysql_db(self, mySQLTreeWidget, statusBar):
        self.mySQL_utils.load_and_connect_db(statusBar)

        self.fill_mysql_tree(mySQLTreeWidget)

    def create_mysql_database(self, new_database_name, mySQLTreeWidget, statusBar):
        matched_items = mySQLTreeWidget.findItems(new_database_name, Qt.MatchContains, 0)
        if len(matched_items) > 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Database with that name already exists.")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

        elif new_database_name == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Database name not set.")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

        elif self.mySQL_utils.check_connection():
            self.mySQL_utils.create_database(new_database_name, statusBar)
            self.fill_mysql_tree(mySQLTreeWidget)

    def delete_selected_mysql_database(self, mySQLTreeWidget, statusBar):
        selected_items = mySQLTreeWidget.selectedItems()
        for selected_item in selected_items:
            database_name = selected_item.text(0)
            self.mySQL_utils.delete_database(database_name, statusBar)
        
        self.fill_mysql_tree(mySQLTreeWidget)

    # def load_collections(self, current_database_name, collectionsComboBox):
    #     table_names_typle = self.mySQL_utils.get_all_tables(current_database_name)
    #     collectionsComboBox.clear()
    #     collectionsComboBox.addItems([table_name[0] for table_name in table_names_typle])

    def fill_mysql_tree(self, mySQLTreeWidget):
        mySQLTreeWidget.clear()

        databases_typle = self.mySQL_utils.get_all_databases()

        if databases_typle is None:
            return
        else:
            for database in databases_typle:
                database_item = QTreeWidgetItem(mySQLTreeWidget)
                database_name = database[0]
                database_item.setText(0, database_name)
                table_names_typle = self.mySQL_utils.get_all_tables(database_name)

                for table in table_names_typle:
                    table_item = QTreeWidgetItem(database_item)
                    table_name = table[0]
                    table_item.setText(0, table_name)

    def add_mysql_table_tab(self, database_name, table_name, dataTabWidget, statusBar):
        mySQL_tab_viewer = MySQLTabViewer(database_name, table_name, statusBar)
        dataTabWidget.addTab(mySQL_tab_viewer, table_name)
        dataTabWidget.setCurrentWidget(mySQL_tab_viewer)


    #Mongo load and connect database
    def load_and_connect_mongodb(self, mongoDBTreeWidget, statusBar):
        self.mongo_utils.load_and_connect_db(statusBar)

        self.fill_mongo_tree(mongoDBTreeWidget)
    
    def create_mongo_database(self, new_database_name, mongoDBTreeWidget, statusBar):
        matched_items = mongoDBTreeWidget.findItems(new_database_name, Qt.MatchContains, 0)
        if len(matched_items) > 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Database with that name already exists.")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

        elif new_database_name == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Database name not set.")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

        #elif self.mySQL_utils.check_connection():
        self.mongo_utils.create_database(new_database_name, statusBar)
        self.fill_mongo_tree(mongoDBTreeWidget)

    #Mongo - fill tree view with elements

    def fill_mongo_tree(self, mongoDBTreeWidget):
        mongoDBTreeWidget.clear()

        databases = self.mongo_utils.get_all_databases()
        if databases == None:
            return
        else:
            for database_name in databases:
                mongo_database_item = QTreeWidgetItem(mongoDBTreeWidget)
                mongo_database_item.setText(0, database_name)
                mongo_db_collections = self.mongo_utils.get_all_tables(database_name)
                collections = self.mongo_utils.get_all_tables(database_name)

                for collection in collections:
                    collection_item = QTreeWidgetItem(mongo_database_item)
                    collection_item.setText(0, collection)
    
    def add_mongo_table_tab(self, database_name, table_name, dataTabWidget, statusBar):
        mongoDB_viewer = MongoTabViewer(database_name, table_name, statusBar)
        dataTabWidget.addTab(mongoDB_viewer, table_name)
        dataTabWidget.setCurrentWidget(mongoDB_viewer)

    def delete_selected_mongodb(self, mongoDBTreeWidget, statusBar):
        selected_items = mongoDBTreeWidget.selectedItems()
        if len(selected_items) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("You need to select database before deleting it.")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            for selected_item in selected_items:
                database_name = selected_item.text(0)
                self.mongo_utils.delete_database(database_name, statusBar)
            
            self.fill_mongo_tree(mongoDBTreeWidget)


    # def delete_row(self, databaseDataTableWidget, database_name, collection_name):
    #     row_id = databaseDataTableWidget
    #     self.mySQL_utils.delete_row(database_name, collection_name, )