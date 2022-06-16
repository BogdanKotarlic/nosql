from pyArango.connection import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from utils.load_config import load_config

class ArangoUtils:
    class __ArangoUtils:
        def __init__(self):
                self.mydb = None

        def load_and_connect_db(self, statusBar):
            dialog = QtWidgets.QFileDialog()
            if dialog.exec_():
                filenames = dialog.selectedFiles()
                config_filepath = filenames[0]
                config_json = load_config(config_filepath)

                try: 
                    self.mydb = Connection(
                        username=config_json["username"],
                        password=config_json["password"]
                    )

                    statusBar.showMessage("Connection made!")
                    print("Connection made!")
                except Exception as e:
                    print(e)
                    statusBar.showMessage("Error In Connection")

        def create_database(self, new_database_name, statusBar):
            try:
                self.mydb.createDatabase(name=new_database_name)
                statusBar.showMessage("New Database Created.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Creating new database failed.")

        def create_collection(self, new_collection_name, statusBar):
            try:
                self.mydb.createCollection(name=new_collection_name)
                statusBar.showMessage("New Collection Created.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Creating new collection failed.")

        def create_document(self, new_document, collection, statusBar):
            try:
                bind = { "doc": new_document, "collection": collection }
                query = "INSERT @doc INTO @collection LET newDoc = NEW RETURN newDoc"
                query_result = self.mydb.AQLQuery(query, bindVars=bind)

                print(query_result)
                statusBar.showMessage("New Document Created.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Creating new document failed.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Some entered values are of wrong type.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def get_document(self, document, statusBar):
            try:
                bind = { "doc": document }
                query = "RETURN DOCUMENT(@doc)"
                query_result = self.mydb.AQLQuery(query, bindVars=bind)

                print(query_result)
                statusBar.showMessage("Document retrieved successfully.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Reading document failed.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Reading document failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def update_document(self, key, document, collection, new_values, statusBar):
            try:
                bind = { key, document, collection, new_values }
                query = "UPDATE @key WITH {*@new_values} IN @document"
                query_result = self.mydb.AQLQuery(query, bindVars=bind)

                print(query_result)
                statusBar.showMessage("Document updated.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Updating document failed.")

        def remove_document(self, key, collection, statusBar):
            try:
                bind = { 
                    "key": key,
                    "collection": collection
                }

                query = "REMOVE @key IN @collection"
                query_result = self.mydb.AQLQuery(query, bindVars=bind)

                print(query_result)
                statusBar.showMessage("Docunebt removed.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Removing document failed.")

    instance = None
    def __init__(self):
        if not ArangoUtils.instance:
            ArangoUtils.instance = ArangoUtils.__ArangoUtils()
        else:
            pass

    def __getattr__(self, name):
        return getattr(self.instance, name)
