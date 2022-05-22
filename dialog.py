from dialog_select import DialogSelect
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql_functions
from functools import partial
import spec

class Dialog(QtWidgets.QDialog):
    def __init__(self, db_name, table_name, data, mode):
        super().__init__()

        self.new = None

        mysql_spec = spec.load_spec()
        table_spec = {}
        if table_name in mysql_spec.keys():
            table_spec = mysql_spec[table_name]

        self.search_results = []

        columns = [column[0] for column in mysql_functions.show_columns(db_name, table_name)]


        self.setWindowTitle("Dialog")

        self.layout = QtWidgets.QVBoxLayout()

        self.texts = []

        for column in columns:
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.label = QtWidgets.QLabel(self)
            self.label.setObjectName(column)
            self.label.setText(column)
            self.horizontalLayout.addWidget(self.label)
            self.lineEdit = QtWidgets.QLineEdit(self)
            self.lineEdit.setObjectName(column+"lineEdit")
            self.horizontalLayout.addWidget(self.lineEdit)
            self.texts.append(self.lineEdit)

            if column in table_spec.keys():
                self.selectButton = QtWidgets.QPushButton(self)
                self.selectButton.setObjectName("selectButton")
                self.selectButton.setText("Select")
                self.selectButton.clicked.connect(partial(self.select, db_name, table_spec[column], columns, column))
                self.horizontalLayout.addWidget(self.selectButton)
                self.newButton = QtWidgets.QPushButton(self)
                self.newButton.setObjectName("newButton")
                self.newButton.setText("New")
                self.newButton.clicked.connect(partial(self.new_dialog, db_name, table_spec[column], columns, column))
                self.horizontalLayout.addWidget(self.newButton)

            self.layout.addLayout(self.horizontalLayout)

        self.button = QtWidgets.QPushButton(self)

        if mode == "update":
            for i, t in enumerate(self.texts):
                t.setText(str(data[i]))
            self.button.setObjectName("updateButton")
            self.button.setText("Update")
            self.button.clicked.connect(partial(self.update, db_name, table_name, columns))
        elif mode == "insert":
            self.button.setObjectName("insertButton")
            self.button.setText("Insert")
            self.button.clicked.connect(partial(self.insert, db_name, table_name, columns))
        elif mode == "search":
            self.button.setObjectName("searchButton")
            self.button.setText("Search")
            self.button.clicked.connect(partial(self.search, db_name, table_name, columns))
        elif mode == "new":
            self.button.setObjectName("insertButton")
            self.button.setText("Insert")
            self.button.clicked.connect(partial(self.insert_new, db_name, table_name, columns, data))



        self.layout.addWidget(self.button)
        self.setLayout(self.layout)


    def insert(self, db_name, table_name, columns):
        values = tuple([text.text().strip() for text in self.texts])
        mysql_functions.insert(db_name, table_name, columns, values)
        self.clear_all()

    def clear_all(self):
        for t in self.texts:
            t.clear()

    def update(self, db_name, table_name, columns):
        values = tuple([text.text().strip() for text in self.texts])
        mysql_functions.update(db_name, table_name, columns, values)
        self.close()

    def search(self, db_name, table_name, columns):
        values = tuple([text.text().strip() for text in self.texts])
        
        self.search_results = [result for result in mysql_functions.search(db_name, table_name, columns, values)]
        self.close()

    def get_search_results(self):
        return self.search_results

    def select(self, db_name, table_name, columns, column):
        dlg = DialogSelect(db_name, table_name, column)
        closed = dlg.exec()
        if not closed:
            selected = dlg.get_selected()
            self.texts[columns.index(column)].setText(selected)


    def new_dialog(self, db_name, table_name, columns, column):
        dlg = Dialog(db_name, table_name, column, "new")
        closed = dlg.exec()
        if not closed:
            new = dlg.get_new()
            self.texts[columns.index(column)].setText(new)

    def get_new(self):
        return self.new

    def insert_new(self, db_name, table_name, columns, column):
        self.new = self.texts[columns.index(column)].text().strip()
        self.insert(db_name, table_name, columns)
        self.close()