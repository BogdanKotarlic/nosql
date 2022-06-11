from PyQt5 import QtWidgets
from PyQt5 import QtCore

from utils.mongo_utils import MongoUtils
from mongoDB_component.mongoDB_controller import MongoController

class MongoTabViewer(QtWidgets.QWidget):
    def __init__(self, database_name, table_name, statusBar, parent=None):
        super().__init__(parent=parent)

        self.database_name = database_name
        self.table_name = table_name
        self.statusBar = statusBar
        self.mongo_controller = MongoController()

        self.setObjectName("mongoTabViewer")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(5, 10, 600, 460))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.DataVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.DataVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.DataVerticalLayout.setObjectName("DataVerticalLayout")

        self.dataTableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.dataTableWidget.setObjectName("dataTableView")
        self.DataVerticalLayout.addWidget(self.dataTableWidget)

        self.load_table_data()
    
    def load_table_data(self):
        self.mongo_controller.load_table_data(self.database_name, self.table_name, self.dataTableWidget)