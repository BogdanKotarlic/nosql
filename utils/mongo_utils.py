from hashlib import new
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pymongo

from utils.load_config import load_config

class MongoUtils:
    class __MongoUtils:
        def __init__(self):
            self.mydb = None
        
        def load_and_connect_db(self, statusBar):
            dialog = QtWidgets.QFileDialog()
            if dialog.exec_():
                filenames = dialog.selectedFiles()
                config_filepath = filenames[0]
                config_json = load_config(config_filepath)
                print(config_json)

                try: 
                    self.mydb = pymongo.MongoClient(
                        "mongodb://" + load_config(config_filepath)["host"]
                    )
                    statusBar.showMessage("Connection made!")
                    print("Connection made!")
                    #print(self.mydb.list_database_names)
                except Exception as e:
                    print(e)
                    statusBar.showMessage("Error In Connection")  
        
        def create_database(self, new_database_name, statusBar):
            try:
                #dodat test jer drugacije mongodb ne moze kreirati novu db
                new_db = self.mydb[new_database_name]
                test = new_db.test
                tes = {}
                test.insert_one(tes)
                statusBar.showMessage("New Database Created.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Creating new database failed.")

        def get_all_databases(self):
            databases = []
            if self.mydb == None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("You need to connect first.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
            else:
                for i in self.mydb.list_database_names():
                    databases.append(i)

                return databases

        def get_all_tables(self, mongodb_name):
            collections = []

            for i in self.mydb[mongodb_name].list_collection_names():
                collections.append(i)

            return collections
        
        def get_table_data(self, database_name, table_name):
            try:
                db = self.mydb[database_name]
                col = db[table_name]
                return col.find()
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Getting table data failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        
        def delete_database(self, mongodb_name, statusBar):
            self.mydb.drop_database(mongodb_name)
            statusBar.showMessage("Mongo database dropped.")

            

    
    instance = None
    def __init__(self):
        if not MongoUtils.instance:
            MongoUtils.instance = MongoUtils.__MongoUtils()
        else:
            pass
    def __getattr__(self, name):
        return getattr(self.instance, name)