from PyQt5 import QtWidgets
from PyQt5 import QtCore

from utils.mysql_utils import MySQLUtils
from mySQL_tab_component.mySQL_tab_controller import MySQLTabController


class MySQLTabViewer(QtWidgets.QWidget):
    def __init__(self, database_name, table_name, statusBar, CRUDActionsViewer, parent=None):
        super().__init__(parent=parent)

        self.CRUDActionsViewer = CRUDActionsViewer

        self.setObjectName("mySQLTabViewer")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(5, 10, 600, 460))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.DataVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.DataVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.DataVerticalLayout.setObjectName("DataVerticalLayout")

        # Deo za prikaz tabele MySQL baze
        self.dataTableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.dataTableWidget.setObjectName("dataTableView")
        self.header = self.dataTableWidget.horizontalHeader()
        self.DataVerticalLayout.addWidget(self.dataTableWidget)

        # obavezno polje
        self.tab_controller = MySQLTabController(database_name, table_name, statusBar, self.dataTableWidget, self.DataVerticalLayout)

        self.dataTableWidget.clicked.connect(lambda x: self.tab_controller.change_controller_for_CRUDActionViewer(CRUDActionsViewer))
        self.header.sectionClicked.connect(lambda x: self.tab_controller.change_controller_for_CRUDActionViewer(CRUDActionsViewer))
        
        self.load_table_data()

    def load_table_data(self):
        self.tab_controller.load_table_data()