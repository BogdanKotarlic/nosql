from PyQt5 import QtWidgets
from utils.mysql_utils import MySQLUtils
from data_handler_dialog.table_reference_spec import load_spec
from functools import partial

from data_handler_dialog.dialog_select import DialogSelect


class DataHandlerDialog(QtWidgets.QWidget):
    def __init__(self, db_name, table_name, data, mode, statusBar, dataTableWidget, tab_controller, tab_model, DataVerticalLayout, parent=None):
        super().__init__(parent=parent)
        # self.move(1400, 200)
        self.new = None
        self.mySQL_utils = MySQLUtils()
        self.statusBar = statusBar
        self.tab_controller = tab_controller
        self.tab_model = tab_model
        self.dataTableWidget = dataTableWidget 
        self.values_with_keys = []
        self.select_clicked = False
        self.parentDataVerticalLayout = DataVerticalLayout

        mysql_spec = load_spec()
        table_spec = {}
        self.id_column_name = ""
        self.id_column_value = 0
        if table_name in mysql_spec.keys():
            table_spec = mysql_spec[table_name]["ref"]
            self.id_column_name = mysql_spec[table_name]["id_col"]
            # print("table spec", table_spec)

        columns = [column[0]
                   for column in self.mySQL_utils.get_table_columns(db_name, table_name)]
        self.db_name = db_name
        self.table_name = table_name
        self.columns = columns
        self.columns_with_references = []

        self.search_results = []

        self.setWindowTitle("Dialog")

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

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
            self.lineEdit.setObjectName(column+"LineEdit")
            self.horizontalLayout.addWidget(self.lineEdit)
            self.texts.append(self.lineEdit)

            if column in table_spec.keys():
                self.columns_with_references.append(column)
                self.selectButton = QtWidgets.QPushButton(self)
                self.selectButton.setObjectName(column+"SelectButton")
                self.selectButton.setText("Select")
                # tabela koju referencira - table_spec[column][0], polje tabele koju referencira - table_spec[column][1], polje tabele koja referencira
                self.selectButton.clicked.connect(partial(self.select, table_spec[column][0], table_spec[column][1], column))
                self.horizontalLayout.addWidget(self.selectButton)
                
            if column == self.id_column_name:
                self.label.setVisible(False)
                self.lineEdit.setVisible(False)
            self.layout.addLayout(self.horizontalLayout)

        self.button = QtWidgets.QPushButton(self)

        if mode == "update":
            for i, t in enumerate(self.texts):
                t.setText(str(data[i]))
            self.button.setObjectName("updateButton")
            self.button.setText("Update")
            self.button.clicked.connect(self.update)
        elif mode == "insert":
            self.button.setObjectName("insertButton")
            self.button.setText("Insert")
            self.button.clicked.connect(self.insert)
        elif mode == "search":
            self.button.setObjectName("searchButton")
            self.button.setText("Search")
            self.button.clicked.connect(self.search)
        elif mode == "new":
            self.button.setObjectName("insertButton")
            self.button.setText("Insert")
            self.button.clicked.connect(partial(self.insert_new, data))

        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setObjectName("closeButton")
        self.close_button.setText("Close")
        self.close_button.clicked.connect(self.remove_dialog)

        # self.actionLine = QtWidgets.QHBoxLayout(self)
        # self.actionLine.addWidget(self.button)
        # self.actionLine.addWidget(self.close_button)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.close_button)

        # self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def insert(self):
        values = tuple([text.text().strip() for text in self.texts])

        self.mySQL_utils.insert(
            self.db_name, self.table_name, self.columns, values, self.statusBar)
        self.clear_all(self.columns_with_references)
        self.tab_controller.load_table_data(None, True)
        # self.close()

    def update(self):
        new_values = tuple([text.text().strip() for text in self.texts])
        values_with_keys = []
        if self.select_clicked:
            values_with_keys = self.values_with_keys
        else:
            values_with_keys = new_values
        self.mySQL_utils.update(
            self.db_name, self.table_name, self.columns, new_values, values_with_keys, self.statusBar)
        self.tab_controller.load_table_data()
        # self.close()

    def clear_all(self, columns_with_references=None):
        if columns_with_references == None:
            for t in self.texts:
                t.clear()
            return
        for column in self.columns:
            if column not in self.columns_with_references:
                self.texts[self.columns.index(column)].clear()

    def search(self):
        values = tuple([text.text().strip() for text in self.texts])
        results = self.mySQL_utils.search(
            self.db_name, self.table_name, self.columns, values)
        self.search_results = [result for result in results]
        
        self.tab_model.load_table_data(self.db_name, self.table_name, self.dataTableWidget, self.get_search_results())
        # self.close()

    def get_search_results(self):
        return self.search_results

    def select(self, ref_table, ref_column, column):
        self.select_clicked = True
        self.values_with_keys = tuple([text.text().strip() for text in self.texts])
        dlg = DialogSelect(self.db_name, ref_table, ref_column)
        closed = dlg.exec()
        if not closed:
            selected = dlg.get_selected()
            print("selektovano je: ", selected)
            self.texts[self.columns.index(column)].setText(str(selected))

    # def new_dialog(self, ref_table, ref_column, column):
    #     dlg = DataHandlerDialog(self.db_name, ref_table, ref_column, "new", self.statusBar)
    #     closed = dlg.exec()
    #     if not closed:
    #         new = dlg.get_new()
    #         self.texts[self.columns.index(column)].setText(str(new))

    def insert_new(self, column):
        self.new = self.texts[self.columns.index(column)].text().strip()
        self.insert()
        self.close()

    def get_new(self):
        return self.new

    def remove_dialog(self):
        self.tab_controller.old_dialog = None
        self.parentDataVerticalLayout.removeWidget(self)
        self.deleteLater()
