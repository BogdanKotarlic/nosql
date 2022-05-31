from PyQt5 import QtCore, QtGui, QtWidgets

from main_window_controller import MainWindowController


class MainWindowViewer(object):
    def __init__(self):
        self.main_window_controller = MainWindowController()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 580)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # databasesTabWidget
        self.databasesTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.databasesTabWidget.setGeometry(QtCore.QRect(10, 30, 241, 511))
        self.databasesTabWidget.setObjectName("databasesTabWidget")

        # MySQL deo u databasesTabWidget-u
        self.mysqlTab = QtWidgets.QWidget()
        self.mysqlTab.setObjectName("mysqlTab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.mysqlTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(2, 5, 231, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mySQLVerticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.mySQLVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mySQLVerticalLayout.setObjectName("mySQLVerticalLayout")
        #   Deo za prikaz baze i tabela
        self.mySQLTreeWidget = QtWidgets.QTreeWidget(self.verticalLayoutWidget)
        self.mySQLTreeWidget.setObjectName("mySQLTreeWidget")
        self.mySQLTreeWidget.headerItem().setText(0, "Databases:")
        self.mySQLTreeWidget.setColumnCount(1)
        self.mySQLVerticalLayout.addWidget(self.mySQLTreeWidget)
        #   Akcije: konekcija
        self.connectMySQLDBPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.connectMySQLDBPushButton.setObjectName("connectMySQLDBPushButton")
        self.mySQLVerticalLayout.addWidget(self.connectMySQLDBPushButton)
        #   Akcije: brisanje i kreiranje nove baze
        self.deleteMySQLDBPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.deleteMySQLDBPushButton.setObjectName("deleteMySQLDBPushButton")
        self.mySQLVerticalLayout.addWidget(self.deleteMySQLDBPushButton)
        self.createMySQLDBHorizontalLayout = QtWidgets.QHBoxLayout()
        self.createMySQLDBHorizontalLayout.setObjectName("createMySQLDBHorizontalLayout")
        self.newMySQLNameLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.newMySQLNameLineEdit.setObjectName("newMySQLNameLineEdit")
        self.createMySQLDBHorizontalLayout.addWidget(self.newMySQLNameLineEdit)
        self.createMySQLDBPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.createMySQLDBPushButton.setObjectName("createMySQLDBPushButton")
        self.createMySQLDBHorizontalLayout.addWidget(self.createMySQLDBPushButton)
        self.mySQLVerticalLayout.addLayout(self.createMySQLDBHorizontalLayout)
        self.databasesTabWidget.addTab(self.mysqlTab, "")

        # Mongo deo u databasesTabWidget-u
        self.mongoTab = QtWidgets.QWidget()
        self.mongoTab.setObjectName("mongoTab")
        self.databasesTabWidget.addTab(self.mongoTab, "")

        #   Ovde ide Mongo deo za prikaz baza, tabela i akcije

        # Arango deo u databasesTabWidget-u
        self.arangoTab = QtWidgets.QWidget()
        self.arangoTab.setObjectName("arangoTab")
        self.databasesTabWidget.addTab(self.arangoTab, "")

        #   Ovde ide Arango deo za prikaz baza, tabela i akcije

        # Deo za prikaz podataka baza kroz tabove unutar dataTabWidget-a
        self.dataTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.dataTabWidget.setGeometry(QtCore.QRect(260, 30, 621, 511))
        self.dataTabWidget.setObjectName("dataTabWidget")
        self.dataTabWidget.setTabsClosable(True)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.databasesTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # connections
        self.connectMySQLDBPushButton.clicked.connect(lambda x: self.main_window_controller.load_and_connect_mysql_db(self.mySQLTreeWidget, self.statusbar))
 
        self.deleteMySQLDBPushButton.clicked.connect(lambda x: self.main_window_controller.delete_selected_mysql_database(self.mySQLTreeWidget, self.statusbar))
        self.createMySQLDBPushButton.clicked.connect(lambda x: self.main_window_controller.create_mysql_database(self.newMySQLNameLineEdit, self.mySQLTreeWidget, self.statusbar))
        
        self.dataTabWidget.tabCloseRequested.connect(lambda x: self.main_window_controller.close_tab(x, self.dataTabWidget))

        self.mySQLTreeWidget.itemDoubleClicked.connect(lambda y, x: self.main_window_controller.add_mysql_table_tab(y, x, self.dataTabWidget, self.statusbar))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SmartMan"))

        self.connectMySQLDBPushButton.setText(_translate("MainWindow", "Connect Database"))
        self.deleteMySQLDBPushButton.setText(_translate("MainWindow", "Delete Selected Database"))
        self.newMySQLNameLineEdit.setPlaceholderText(_translate("MainWindow", "New Database Name"))
        self.createMySQLDBPushButton.setText(_translate("MainWindow", "Create"))
        self.databasesTabWidget.setTabText(self.databasesTabWidget.indexOf(self.mysqlTab), _translate("MainWindow", "MySQL"))
        self.databasesTabWidget.setTabText(self.databasesTabWidget.indexOf(self.mongoTab), _translate("MainWindow", "MongoDB"))
        self.databasesTabWidget.setTabText(self.databasesTabWidget.indexOf(self.arangoTab), _translate("MainWindow", "ArangoDB"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowViewer()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
