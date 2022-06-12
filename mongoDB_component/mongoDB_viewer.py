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

        self.dataActionsHorizontalLayout = QtWidgets.QHBoxLayout()
        self.dataActionsHorizontalLayout.setObjectName("dataActionsHorizontalLayout")
        self.insertPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.insertPushButton.setObjectName("insertPushButton")
        self.dataActionsHorizontalLayout.addWidget(self.insertPushButton)
        self.updatePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.updatePushButton.setObjectName("updatePushButton")
        self.dataActionsHorizontalLayout.addWidget(self.updatePushButton)
        self.deletePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.deletePushButton.setObjectName("deletePushButton")
        self.dataActionsHorizontalLayout.addWidget(self.deletePushButton)
        self.DataVerticalLayout.addLayout(self.dataActionsHorizontalLayout)

        self.dataTableWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_2)
        self.dataTableWidget.setObjectName("dataTableView")
        self.DataVerticalLayout.addWidget(self.dataTableWidget)
        self.dataTableWidget.itemClicked.connect(self.clicked)

        _translate = QtCore.QCoreApplication.translate
        self.insertPushButton.setText(_translate("MainWindow", "Insert"))
        self.updatePushButton.setText(_translate("MainWindow", "Update Selected"))
        self.deletePushButton.setText(_translate("MainWindow", "Delete Selected"))

        self.load_table_data()

        self.deletePushButton.clicked.connect(lambda y: self.mongo_controller.delete_row(self.database_name, self.table_name, self.dataTableWidget))
        self.insertPushButton.clicked.connect(lambda y: self.mongo_controller.insert(self.database_name, self.table_name, self.dataTableWidget, self.statusBar))
        self.updatePushButton.clicked.connect(lambda y: self.mongo_controller.update(self.database_name, self.table_name, self.dataTableWidget, self.statusBar))
    
    def load_table_data(self):
        self.mongo_controller.load_table_data(self.database_name, self.table_name, self.dataTableWidget)
    
    def clicked(self):
        print("test test")