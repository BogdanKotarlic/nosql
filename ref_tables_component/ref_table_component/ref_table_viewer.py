from PyQt5 import QtWidgets
from PyQt5 import QtCore

from utils.mysql_utils import MySQLUtils
from ref_tables_component.ref_table_component.ref_table_controller import RefTableController


class RefTableViewer(QtWidgets.QWidget):
    def __init__(self, database_name, table_name, statusBar, main_window_controller, CRUDActionsViewer, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("mySQLTabViewer")
        
        self.table_name_label = QtWidgets.QLabel(self)
        self.table_name_label.setGeometry(QtCore.QRect(0, 0, 400, 30))
        self.table_name_label.setText(table_name)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 30, 400, 320))
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
        self.controller = RefTableController(database_name, table_name, statusBar, self.dataTableWidget, self.DataVerticalLayout, main_window_controller)

        self.dataTableWidget.clicked.connect(lambda x: self.controller.change_controller_for_CRUDActionViewer(CRUDActionsViewer))
        
        self.header.sectionClicked.connect(lambda x: self.controller.change_controller_for_CRUDActionViewer(CRUDActionsViewer))

        self.load_table_data()

    def load_table_data(self):
        self.controller.load_table_data()