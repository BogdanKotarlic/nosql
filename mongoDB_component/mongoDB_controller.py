from PyQt5 import QtCore, QtGui, QtWidgets

from mongoDB_component.mongoDB_model import MongoTabModel
from utils.mongo_utils import MongoUtils

class MongoController:
    def __init__(self):
        self.mongo_tab_model = MongoTabModel()
        self.mongo_utils = MongoUtils()
    
    def load_table_data(self, database_name, table_name, dataTableWidget):
        self.mongo_tab_model.load_table_data(database_name, table_name, dataTableWidget)
    
    def delete_row(self, database_name, table_name, dataTableWidget):
        print("Uraditi brisanje")
    
    def insert(self, database_name, table_name, dataTableWidget, statusBar):
        print("Uraditi insert")

    def update(self, database_name, table_name, dataTableWidget, statusBar):
        print("Uraditi update")