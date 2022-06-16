from PyQt5 import QtCore, QtGui, QtWidgets

from main_window_model import MainWindowModel
from utils.mysql_utils import MySQLUtils
from data_handler_dialog.data_handler_dialog import DataHandlerDialog
from data_handler_dialog.table_reference_spec import load_spec
from ref_tables_component.ref_table_component.ref_table_viewer import RefTableViewer

class MainWindowController:
    def __init__(self):
        self.main_window_model = MainWindowModel()
        self.mySQL_utils = MySQLUtils()
        self.data_handler_viewer = None
        self.dataTabWidget = None

    def set_data_tab_widget(self, dataTabWidget):
        self.dataTabWidget = dataTabWidget

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
 
    def add_mysql_table_tab(self, treeItem, column, dataTabWidget, statusBar, CRUDActionsViewer):
        table_name = treeItem.text(column)
        # provera da li je kliknuta tabela ili baza
        if treeItem.parent() != None:
            database_name = treeItem.parent().text(column)
            self.main_window_model.add_mysql_table_tab(database_name, table_name, dataTabWidget, statusBar, CRUDActionsViewer)
    
    def close_tab(self, tab_index, dataTabWidget):
        dataTabWidget.removeTab(tab_index)

    def show_mysql_ref_tables(self, tab_index, dataTabWidget, refTablesViewer, refLabel, MainWindow, statusBar, CRUDActionsViewer):
        refTablesViewer.clear_HBoxLayout()
        if tab_index == -1:
            refTablesViewer.setVisible(False)
            refLabel.setVisible(False)
            MainWindow.resize(900, 600)
            return

        current_viewer = dataTabWidget.currentWidget()
        
        if current_viewer.tab_controller.for_database_type == "mySQL":
            refTablesViewer.setVisible(True)
            refLabel.setVisible(True)
            MainWindow.resize(900, 1000)

            table_name = current_viewer.tab_controller.table_name
            database_name = current_viewer.tab_controller.database_name
            print("table name je:", table_name, ", database name je: ", database_name)

            mysql_spec = load_spec()
            if table_name in mysql_spec.keys():
                ref_spec = mysql_spec[table_name]["ref"]
                referencing_columns = ref_spec.keys()
                if len(referencing_columns) == 0:
                    refTablesViewer.setVisible(False)
                    MainWindow.resize(900, 620)
                    return
                for column in referencing_columns:
                    table_name = ref_spec[column][0]
                    ref_table = RefTableViewer(database_name, table_name, statusBar, self, CRUDActionsViewer, refTablesViewer)
                    refTablesViewer.add_to_HBoxLayout(ref_table)
        else:
            refTablesViewer.setVisible(False)
            refLabel.setVisible(False)
            MainWindow.resize(900, 620)
    
    def update_upper_table(self, database_name, table_name):
        tab_count = self.dataTabWidget.count()
        for tab_index in range(tab_count):
            widget_controller = self.dataTabWidget.widget(tab_index).tab_controller
            if widget_controller.database_name == database_name and widget_controller.table_name == table_name:
                widget_controller.load_table_data()
    
    
    #Mongo
    def add_mongo_table_tab(self, treeItem, column, dataTabWidget, statusBar):
        table_name = treeItem.text(column)
        if treeItem.parent() != None:
            database_name = treeItem.parent().text(column)
            self.main_window_model.add_mongo_table_tab(database_name, table_name, dataTabWidget, statusBar)

    def load_and_connect_mongodb(self, mongoDBTreeWidget, statusBar):
        self.main_window_model.load_and_connect_mongodb(mongoDBTreeWidget, statusBar)
    
    def delete_selected_mongodb(self, mongoDBTreeWidget, statusBar):
        self.main_window_model.delete_selected_mongodb(mongoDBTreeWidget, statusBar)
    
    def create_mongo_database(self, newMongoNameLineEdit, mongoDBTreeWidget, statusBar):
        new_database_name = newMongoNameLineEdit.text()
        newMongoNameLineEdit.clear()
        self.main_window_model.create_mongo_database(new_database_name, mongoDBTreeWidget, statusBar)

    def transform_from_sql_to_mongo(self, mongoDBTreeWidget, statusBar):
        self.main_window_model.transform_to_mongo(mongoDBTreeWidget, statusBar)

    # za sve

    def change_tab_controller_for_CRUDActionViewer(self, tab_index, dataTabWidget, CRUDActionsViewer):
        if tab_index == -1:
            CRUDActionsViewer.set_tab_controller(None)
            return

        current_viewer = dataTabWidget.currentWidget()
        CRUDActionsViewer.set_tab_controller(current_viewer.tab_controller)