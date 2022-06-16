from PyQt5 import QtCore, QtWidgets
from arango_component.arango_controller import ArangoController

class ArangoViewer(QtWidgets.QWidget):
    def __init__(self, database_name, table_name, statusBar, CRUDActionsViewer, parent=None):
        super().__init__(parent=parent)

        self.CRUDActionsViewer = CRUDActionsViewer

        self.setObjectName("arangoViewer")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(5, 10, 600, 460))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.DataVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.DataVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.DataVerticalLayout.setObjectName("DataVerticalLayout")

        # Deo za prikaz tabele Arango baze
        self.dataTableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.dataTableWidget.setObjectName("dataTableView")
        self.header = self.dataTableWidget.horizontalHeader()
        self.DataVerticalLayout.addWidget(self.dataTableWidget)

        self.tab_controller = ArangoController(database_name, table_name, statusBar, self.dataTableWidget, self.DataVerticalLayout)
        
        self.load_table_data()

    def load_table_data(self):
        self.tab_controller.load_table_data()