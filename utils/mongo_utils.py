from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QMessageBox
import pymongo

from utils.load_config import load_config
from utils.datatypes import sql_to_python

class MongoUtils:
    class __MongoUtils:
        def __init__(self):
            self.mydb = None
            self.mycursor = None
        
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
                except Exception as e:
                    print(e)
                    statusBar.showMessage("Error In Connection")  
    
    instance = None
    def __init__(self):
        if not MongoUtils.instance:
            MongoUtils.instance = MongoUtils.__MongoUtils()
        else:
            pass
    def __getattr__(self, name):
        return getattr(self.instance, name)