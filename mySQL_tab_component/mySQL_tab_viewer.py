from PyQt5 import QtWidgets
from PyQt5 import QtCore

from utils.mysql_utils import MySQLUtils
from mySQL_tab_component.mySQL_tab_controller import MySQLTabController


class MySQLTabViewer(QtWidgets.QWidget):
    def __init__(self, database_name, table_name, statusBar, parent=None):
        super().__init__(parent=parent)

        self.database_name = database_name
        self.table_name = table_name
        self.statusBar = statusBar
        self.mySQL_tab_controller = MySQLTabController()

        self.setObjectName("mySQLTabViewer")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(5, 10, 600, 460))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.DataVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.DataVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.DataVerticalLayout.setObjectName("DataVerticalLayout")

        # CRUD deo za MySQL u dataTabWidget-u
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
        self.getAllPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.getAllPushButton.setObjectName("getAllPushButton")
        self.dataActionsHorizontalLayout.addWidget(self.getAllPushButton)
        self.searchPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.searchPushButton.setObjectName("searchPushButton")
        self.dataActionsHorizontalLayout.addWidget(self.searchPushButton)
        self.DataVerticalLayout.addLayout(self.dataActionsHorizontalLayout)

        # Deo za prikaz tabele MySQL baze
        self.dataTableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.dataTableWidget.setObjectName("dataTableView")
        self.DataVerticalLayout.addWidget(self.dataTableWidget)

        _translate = QtCore.QCoreApplication.translate
        self.insertPushButton.setText(_translate("MainWindow", "Insert"))
        self.updatePushButton.setText(_translate("MainWindow", "Update Selected"))
        self.deletePushButton.setText(_translate("MainWindow", "Delete Selected"))
        self.getAllPushButton.setText(_translate("MainWindow", "Get All"))
        self.searchPushButton.setText(_translate("MainWindow", "Search"))

        self.load_table_data()

        # connections
        self.getAllPushButton.clicked.connect(lambda y: self.mySQL_tab_controller.load_table_data(self.database_name, self.table_name, self.dataTableWidget))
        self.deletePushButton.clicked.connect(lambda y: self.mySQL_tab_controller.delete_row(self.database_name, self.table_name, self.dataTableWidget))
        self.insertPushButton.clicked.connect(lambda y: self.mySQL_tab_controller.show_data_handler_dialog(self.database_name, self.table_name, "insert", self.dataTableWidget, self.statusBar))
        self.updatePushButton.clicked.connect(lambda y: self.mySQL_tab_controller.show_data_handler_dialog(self.database_name, self.table_name, "update", self.dataTableWidget, self.statusBar))
        self.searchPushButton.clicked.connect(lambda y: self.mySQL_tab_controller.show_data_handler_dialog(self.database_name, self.table_name, "search", self.dataTableWidget, self.statusBar))

    def load_table_data(self):
        self.mySQL_tab_controller.load_table_data(self.database_name, self.table_name, self.dataTableWidget)