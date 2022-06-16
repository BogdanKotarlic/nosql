from PyQt5 import QtCore, QtGui, QtWidgets

# from mySQL_tab_component.mySQL_tab_model import MySQLTabModel
from ref_tables_component.ref_table_component.ref_table_model import RefTableModel
from utils.mysql_utils import MySQLUtils
from data_handler_dialog.data_handler_dialog import DataHandlerDialog

class RefTableController:
    def __init__(self, database_name, table_name, statusBar, dataTableWidget, DataVerticalLayout, main_window_controller):
        # obavezno polje
        self.for_database_type = "mySQL"
        
        self.ref_table_model = RefTableModel()
        self.database_name = database_name
        self.table_name = table_name
        self.statusBar = statusBar
        self.dataTableWidget = dataTableWidget
        self.DataVerticalLayout = DataVerticalLayout
        self.main_window_controller = main_window_controller
        self.mySQL_utils = MySQLUtils()
        self.old_dialog = None
        self.first_time_loading = True
    
    def load_table_data(self, table_data=None, mark_new_row=False):
        self.ref_table_model.load_table_data(self.database_name, self.table_name, self.dataTableWidget, table_data, mark_new_row)
        if self.first_time_loading == False:
            self.main_window_controller.update_upper_table(self.database_name, self.table_name)
        self.first_time_loading = False

    def delete_row(self):
        row_index = self.dataTableWidget.currentRow()
        row_data_id = self.dataTableWidget.item(row_index, 0).text()
        delete_done = self.mySQL_utils.delete_row(self.database_name, self.table_name, row_data_id)
        if delete_done:
            self.load_table_data()

    def show_data_handler_dialog(self, mode):
        if mode == "insert":
            if self.old_dialog != None:
                self.old_dialog.remove_dialog()
                print("uklonjen stari dialog")
            dlg = DataHandlerDialog(self.database_name, self.table_name, None, mode, self.statusBar, self.dataTableWidget, self, self.ref_table_model, self.DataVerticalLayout)
            self.DataVerticalLayout.addWidget(dlg)
            self.old_dialog = dlg
            print("dodat novi dialog")
        elif mode == "update":
            if self.old_dialog != None:
                self.old_dialog.remove_dialog()
            data = [record for record in self.mySQL_utils.get_table_data(self.database_name, self.table_name)]
            selected_indexes = self.dataTableWidget.selectedIndexes()
            for s in selected_indexes:
                dlg = DataHandlerDialog(self.database_name, self.table_name, data[s.row()], mode, self.statusBar, self.dataTableWidget, self, self.ref_table_model, self.DataVerticalLayout)
                self.DataVerticalLayout.addWidget(dlg)
                self.old_dialog = dlg
        elif mode == "search":
            if self.old_dialog != None:
                self.old_dialog.remove_dialog()
            dlg = DataHandlerDialog(self.database_name, self.table_name, None, mode, self.statusBar, self.dataTableWidget, self, self.ref_table_model, self.DataVerticalLayout)
            self.DataVerticalLayout.addWidget(dlg)
            self.old_dialog = dlg

    def change_controller_for_CRUDActionViewer(self, CRUDActionsViewer):
        CRUDActionsViewer.set_tab_controller(self)