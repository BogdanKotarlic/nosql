from PyQt5 import QtWidgets
from PyQt5 import QtCore

class CRUDActionsViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tab_controller = None
        self.once_connected = False

        self.setObjectName("CRUDActionsViewer")
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(5, 10, 600, 30))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        # self.verticalLayoutWidget.setStyleSheet("border: 1px solid red")

        self.dataActionsHorizontalLayout = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.dataActionsHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.dataActionsHorizontalLayout.setObjectName("dataActionsHorizontalLayout")
        self.insertPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.insertPushButton.setObjectName("insertPushButton")
        self.dataActionsHorizontalLayout.addWidget(self.insertPushButton)
        self.updatePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.updatePushButton.setObjectName("updatePushButton")
        self.dataActionsHorizontalLayout.addWidget(self.updatePushButton)
        self.deletePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.deletePushButton.setObjectName("deletePushButton")
        self.dataActionsHorizontalLayout.addWidget(self.deletePushButton)
        self.getAllPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.getAllPushButton.setObjectName("getAllPushButton")
        self.dataActionsHorizontalLayout.addWidget(self.getAllPushButton)
        self.searchPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.searchPushButton.setObjectName("searchPushButton")
        self.dataActionsHorizontalLayout.addWidget(self.searchPushButton)

        _translate = QtCore.QCoreApplication.translate
        self.insertPushButton.setText(_translate("CRUDActionsViewer", "Insert"))
        self.updatePushButton.setText(_translate("CRUDActionsViewer", "Update Selected"))
        self.deletePushButton.setText(_translate("CRUDActionsViewer", "Delete Selected"))
        self.getAllPushButton.setText(_translate("CRUDActionsViewer", "Get All"))
        self.searchPushButton.setText(_translate("CRUDActionsViewer", "Search"))


    def set_tab_controller(self, tab_controller):
        print("tab kontroler: ", tab_controller)
        if tab_controller != None:
            print("setting new tab controller")
            self.tab_controller = tab_controller
            database_type = self.tab_controller.for_database_type
            self.set_connections(database_type)
        else:
            print("disconnecting actions")
            self.tab_controller = None
            self.disconnect_actions()
    
    def set_connections(self, database_type):
        if self.once_connected == True:
            print("disconnecting first")
            self.disconnect_actions()

        if database_type == "mySQL":
            print("connecting for mysql")
            self.getAllPushButton.clicked.connect(lambda y: self.tab_controller.load_table_data())
            self.deletePushButton.clicked.connect(lambda y: self.tab_controller.delete_row())
            self.insertPushButton.clicked.connect(lambda y: self.tab_controller.show_data_handler_dialog("insert"))
            self.updatePushButton.clicked.connect(lambda y: self.tab_controller.show_data_handler_dialog("update"))
            self.searchPushButton.clicked.connect(lambda y: self.tab_controller.show_data_handler_dialog("search"))
            self.once_connected = True
        elif database_type == "mongo":
            pass
        elif database_type == "arango":
            pass
    
    def no_tab_controller_set(self):
        print("no controller set")

    def disconnect_actions(self):
        self.getAllPushButton.clicked.disconnect()
        self.deletePushButton.clicked.disconnect()
        self.insertPushButton.clicked.disconnect()
        self.updatePushButton.clicked.disconnect()
        self.searchPushButton.clicked.disconnect()
        self.once_connected = False