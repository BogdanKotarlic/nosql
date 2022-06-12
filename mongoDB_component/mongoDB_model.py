from lib2to3.pytree import convert
from textwrap import indent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QListView
from PyQt5.QtCore import Qt

from utils.mongo_utils import MongoUtils
import json
from bson.json_util import loads, dumps

class MongoTabModel: 
    def __init__(self):
        self.mongo_utils = MongoUtils()

    def load_table_data(self, database_name, table_name, dataTableWidget, table_data=None):
        if table_data == None:
            table_data = self.mongo_utils.get_table_data(database_name, table_name)
        
        data = []
        for i in table_data:
            data.append(i)

        converted = dumps(data, indent=4, sort_keys=True)

        dataTableWidget.addItem(converted)
    