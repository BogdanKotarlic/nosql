from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QMessageBox

from utils.load_config import load_config
from utils.datatypes import sql_to_python

class MySQLUtils:
    class __MySQLUtils:
        def __init__(self):
            self.mydb = None
            self.mycursor = None

        def load_and_connect_db(self, statusBar):
            dialog = QtWidgets.QFileDialog()
            if dialog.exec_():
                filenames = dialog.selectedFiles()
                config_filepath = filenames[0]
                config_json = load_config(config_filepath)

                try: 
                    self.mydb = mysql.connector.connect(
                        host=config_json["host"],
                        user=config_json["user"],
                        password=config_json["password"]
                    )
                    self.mycursor = self.mydb.cursor()
                    statusBar.showMessage("Connection made!")
                    print("Connection made!")
                except Exception as e:
                    print(e)
                    statusBar.showMessage("Error In Connection")                
        
        def create_database(self, new_database_name, statusBar):
            try:
                sql = "CREATE DATABASE IF NOT EXISTS %s" % new_database_name
                self.mycursor.execute(sql)
                statusBar.showMessage("New Database Created.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Creating new database failed.")

        def get_all_databases(self):
            try:
                self.mycursor.execute("SHOW DATABASES")
                dbs = self.mycursor.fetchall()
                return dbs
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Getting all databases failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def get_all_tables(self, database_name):
            try:
                sql = "USE %s" % database_name
                self.mycursor.execute(sql)
                self.mycursor.execute("SHOW TABLES")
                tables = self.mycursor.fetchall()
                return tables
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Getting all tables failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def get_table_data(self, table_name):
            try:
                sql = "SELECT * FROM %s" % table_name
                self.mycursor.execute(sql)
                table_data = self.mycursor.fetchall()
                return table_data
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Getting table data failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def get_table_row_count(self, table_name):
            try:
                sql = "SELECT COUNT(*) FROM %s" % table_name
                self.mycursor.execute(sql)
                row_count = self.mycursor.fetchall()
                return row_count
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Getting table row count failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def get_table_columns(self, table_name):
            try:
                sql = "SHOW COLUMNS FROM %s" % table_name
                self.mycursor.execute(sql)
                table_columns = self.mycursor.fetchall()
                return table_columns
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Getting table columns failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def delete_row(self, database_name, collection_name, row_id):
            contained_data = load_config("config files\mysql_contained_data.json")
            print(collection_name in contained_data)
            if collection_name not in contained_data:
                try:
                    sql = "DELETE FROM %s WHERE id = %s" % (collection_name, row_id)
                    self.mycursor.execute(sql)
                    self.mydb.commit()
                    return True
                except Exception as e:
                    print(e)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Deleting row failed.")
                    msg.setWindowTitle("Info")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    return False
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                text = ("Deleting failed, collections: "+', '.join(['%s']*len(contained_data[collection_name]))+" reference this data.") % tuple(contained_data[collection_name])
                msg.setText(text)
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                return False

        def delete_database(self, database_name, statusBar):
            try:
                sql = "DROP DATABASE %s" % database_name
                self.mycursor.execute(sql)
                statusBar.showMessage("Database dropped.")
                return True
            except Exception as e:
                print(e)
                statusBar.showMessage("Dropping database failed.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Deleting database failed.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
            return False
        
        def insert(self, database_name, table_name, columns, values, statusBar):
            try:
                sql = "INSERT INTO " + table_name + "("  # (name, address) VALUES (%s, %s)"
                first = False
                for index, column in enumerate(columns):
                    if values[index].strip() == "":
                        continue
                    if first:
                        sql += ", "
                    sql += column
                    first = True
                sql += ") VALUES ("
                first = False
                for index, v in enumerate(values):
                    if v.strip() == "":
                        continue
                    if first:
                        sql += ", "
                    sql += "%s"
                    first = True
                sql += ")"
                values = tuple([v for v in values if v != ""])
                types = [column for column in self.get_table_columns(table_name)]
                values = sql_to_python(values, types)

                self.mycursor.execute(sql, values)
                self.mydb.commit()
                statusBar.showMessage("Insert successful.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Insert unsuccessful.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Some entered values are of wrong type.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def update(self, database_name, table_name, columns, values, statusBar):
            try:
                sql = "UPDATE " + table_name + " SET "
                sql_values = []
                for index, column in enumerate(columns):
                    if index > 0 and index < len(columns):
                        sql += ", "
                    sql += column + " = " + "%s"
                    sql_values.append(str(values[index]))
                sql += " WHERE "
                columns_data = [column for column in self.get_table_columns(table_name)]
                first = False
                for index, column in enumerate(columns_data):
                    if column[3] == "PRI":
                        if first and index > 0 and index < len(columns_data):
                            sql += ", "
                        sql += columns[index] + " = " + "%s"
                        sql_values.append(str(values[index]))
                        first = True
                self.mycursor.execute(sql, sql_values)
                self.mydb.commit()
                statusBar.showMessage("Update successful.")
            except Exception as e:
                print(e)
                statusBar.showMessage("Update unsuccessful.")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Update not successful.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def search(self, database_name, table_name, columns, values):
            try:
                sql = "SELECT * FROM " + table_name + " WHERE "
                sql_values = []
                for index, column in enumerate(columns):
                    if values[index].strip() == "":
                        continue
                    if index > 0 and index < len(columns) and len(sql_values) > 0:
                        sql += " AND "
                    sql += column + " = " + "%s"
                    sql_values.append(str(values[index]))
                print(sql)
                self.mycursor.execute(sql, sql_values)
                return self.mycursor
            except Exception as e:
                print(e)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Search not successful.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        def check_connection(self):
            if self.mycursor != None:
                return True
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Connection not made.")
                msg.setWindowTitle("Info")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                return False
        

            
    instance = None
    def __init__(self):
        if not MySQLUtils.instance:
            MySQLUtils.instance = MySQLUtils.__MySQLUtils()
        else:
            pass
    def __getattr__(self, name):
        return getattr(self.instance, name)
