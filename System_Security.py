import csv
import re
import subprocess
import sys
import os
import winreg as wrg
import re
from pdfminer.high_level import extract_text
from PySide6 import QtWidgets
from PySide6.QtWidgets import *
import ctypes
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt
#  pyside6-uic audit_ui.ui -o audit_ui.py


from audit_ui import Ui_Zero_Security
from splash_ui import Ui_Splash

cwd = os.getcwd()
pdf_to_csv_file = "extracted_registry_lines_serialized.csv"
registry_check_file = "registry_check_results.csv"

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

class SplashScreen(QSplashScreen, Ui_Splash):

    def __init__(self):

        super(SplashScreen, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)

    def progress(self):
        for i in range(100):
            time.sleep(0.1)
            self.progressBar.setValue(i)

class MainWindow(QtWidgets.QWidget,Ui_Zero_Security):

    def browse_file(self):
        self.cancel_button()

        file = QFileDialog.getOpenFileName(self, 'Open', cwd,'*.pdf')
        self.path.setText(file[0])

    def file_path(self, path):
        return os.path.join(cwd, path)

    def path_extract(self):
        if self.path.text() != "":
            try:
                path = self.path.text()
                selected_registry = self.dropbox.currentText()
                registry_map = {
                    "HKEY_LOCAL_MACHINE": "HKLM",
                    "HKEY_CLASSES_ROOT": "HKCR",
                    "HKEY_CURRENT_CONFIG": "HKCC",
                    "HKEY_USERS": "HKU",
                    "HKEY_CURRENT_USER": "HKCU"
                }

                if selected_registry in registry_map:
                    registry_abbr = registry_map[selected_registry]
                    txt = extract_text(path)
                    cleaned_text = re.sub(r'(?<!\n)\n(?!\n)', '', txt)
                    pattern = rf"{registry_abbr}\\[A-Za-z0-9_\\\(\)\{{\}}\<\>\s*-]+\:[A-Za-z0-9_\*-\\\(\)\{{\}}\<\>]+"
                    matching_lines = re.findall(pattern, cleaned_text)

                    # Write csv
                    with open(self.file_path(pdf_to_csv_file), mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(['SL', 'LINES'])
                        for idx, line in enumerate(matching_lines, start=1):
                            writer.writerow([idx, line])

                    # read csv
                    with open(self.file_path(pdf_to_csv_file), mode='r', newline='', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        next(reader)
                        tablerow = 0
                        for find in reader:
                            self.path_table.setRowCount(tablerow + 1)
                            self.path_table.setItem(tablerow, 0, QTableWidgetItem(find[1]))
                            tablerow += 1

                else:
                    QMessageBox.warning(self, "Warning", "Please Select a valid option")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Please Select a valid CIS PDF path")

    def registry_checking(self):

        if not self.path_table.item(0, 0) or not self.path_table.item(0, 0).text():
            QMessageBox.warning(self, "Not Found", "No Path Found")
            return

        try:
            row_count = self.path_table.rowCount()
            output_rows = [["sl", "path", "found"]]
            
            location_map = {
                "HKLM": wrg.HKEY_LOCAL_MACHINE,
                "HKCU": wrg.HKEY_CURRENT_USER,
                "HKCR": wrg.HKEY_CLASSES_ROOT,
                "HKU": wrg.HKEY_USERS,
                "HKCC": wrg.HKEY_CURRENT_CONFIG
            }

            for row in range(row_count):
                registry_path = self.path_table.item(row, 0).text() if self.path_table.item(row, 0) else ""

                if not registry_path:
                    QMessageBox.warning(self, "Not Found", f"Row {row + 1} - No registry path found in the table.")
                    continue

                try:
                    location, full_key = registry_path.split("\\", 1)
                    locate, value = full_key.split(":", 1)
                    found = "No"

                    if location in location_map:
                        location_key = location_map[location]
                        try:
                            with wrg.OpenKey(location_key, locate, wrg.KEY_READ) as search_key:
                                try:
                                    wrg.QueryValueEx(search_key, value)
                                    found = "Yes"
                                except FileNotFoundError:
                                    pass
                        except FileNotFoundError:
                            pass

                    output_rows.append([str(row + 1), registry_path, found])
                except Exception:
                    continue

            # Write results to CSV
            with open(self.file_path(registry_check_file), 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerows(output_rows)

            QMessageBox.information(self, "Success", "System checked Successfully")

            # section
            self.path_table.hide()
            self.result_table.show()

            os.remove(self.file_path(pdf_to_csv_file))

            # button
            self.check_security_result.show()
            self.check_security.hide()

            # Populate result table from CSV
            with open(self.file_path(registry_check_file), 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for tablerow, find in enumerate(reader):
                    self.result_table.setRowCount(tablerow + 1)
                    self.result_table.setItem(tablerow, 0, QTableWidgetItem(find[2]))
                    self.result_table.setItem(tablerow, 1, QTableWidgetItem(find[1]))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def cancel_button(self):
        # section
        self.path_table.show()
        self.path_table.setRowCount(0)
        self.dropbox.setCurrentText("Select")
        self.result_table.hide()
        self.dashboard_plot.hide()
        self.hardening_table.hide()
        self.system_info.show()

        # button
        self.check_security.show()
        self.check_security_result.hide()
        self.hardening.hide()
        self.submit_hardening.hide()
   
    def dashboard(self):
        import dashboard
        def clear_layout(layout):
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        # Generate the plots using the dashboard module
        fig1 = dashboard.plot_pie_chart()
        fig2 = dashboard.plot_doughnut_chart()
        fig3 = dashboard.plot_bar_chart_dfr2()
        fig4 = dashboard.plot_bar_chart_dfr3()

        # Create Matplotlib canvases for the figures
        canvas1 = FigureCanvas(fig1)
        canvas2 = FigureCanvas(fig2)
        canvas3 = FigureCanvas(fig3)
        canvas4 = FigureCanvas(fig4)

        # Clear previous widgets in layouts
        clear_layout(self.ax1.layout())
        clear_layout(self.ax2.layout())
        clear_layout(self.ax3.layout())
        clear_layout(self.ax4.layout())

        # Add the new canvases to the layouts
        self.ax1.layout().addWidget(canvas1)
        self.ax2.layout().addWidget(canvas2)
        self.ax3.layout().addWidget(canvas3)
        self.ax4.layout().addWidget(canvas4)

        # Section visibility
        self.dashboard_plot.show()
        self.result_table.hide()
        self.path_table.hide()
        self.system_info.hide()

        # Button visibility
        self.hardening.show()
        self.check_security_result.hide()
     
    def table_hardening(self):
        # section
        self.dashboard_plot.hide()
        self.hardening_table.show()

        # button
        self.submit_hardening.show()
        self.hardening.hide()
        
        # Populate result table from CSV
        with open(self.file_path(registry_check_file), 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            tablerow = 0
            for row in reader:
                if row[2].strip().lower() == "no":
                    self.hardening_table.setRowCount(tablerow + 1)

                    # Add checkbox in the first column
                    checkbox_item = QTableWidgetItem()
                    checkbox_item.setCheckState(Qt.Unchecked)
                    self.hardening_table.setItem(tablerow, 0, checkbox_item)

                    self.hardening_table.setItem(tablerow, 1, QTableWidgetItem(row[1]))
                    tablerow += 1

    def system_hardening(self):
        if not self.hardening_table.item(0, 1) or not self.hardening_table.item(0, 1).text():
            QMessageBox.warning(self, "Not Found", "No Path Found")
            return

        try:
            row_count = self.hardening_table.rowCount()
            any_checked = False
            QMessageBox.warning(self, "Warning", "Please take a backup before proceeding.")

            for row in range(row_count):
                checkbox_item = self.hardening_table.item(row, 0)
                if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                    any_checked = True
                    registry_path = self.hardening_table.item(row, 1).text() if self.hardening_table.item(row, 1) else ""

                    if not registry_path:
                        QMessageBox.warning(self, "Not Found", f"Row {row + 1} - No registry path found in the table.")
                        continue

                    try:
                        location, full_key = registry_path.split("\\", 1)
                        locate, value = full_key.split(":", 1)
                        hardening_status = "Failed"

                        location_map = {
                            "HKLM": wrg.HKEY_LOCAL_MACHINE,
                            "HKCU": wrg.HKEY_CURRENT_USER,
                            "HKCR": wrg.HKEY_CLASSES_ROOT,
                            "HKU": wrg.HKEY_USERS,
                            "HKCC": wrg.HKEY_CURRENT_CONFIG
                        }

                        if location in location_map:
                            location_key = location_map[location]
                            try:
                                # Attempt to create or open the key, handle access denied by bypassing it
                                with wrg.CreateKey(location_key, locate) as key:
                                    wrg.SetValueEx(key, value, 1, wrg.REG_DWORD, 1)
                                hardening_status = "Success"
                            except PermissionError:
                                QMessageBox.warning(self, "Access Denied", f"Access denied to registry key: {registry_path}. You may need to run as administrator.")
                                continue
                            except Exception as e:
                                QMessageBox.warning(self, "Error", f"Error processing row {row + 1}: {e}")

                            QMessageBox.information(self, "Hardening Status", f"{registry_path}\n-> {hardening_status}")
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Error processing row {row + 1}: {e}")
                        continue

            if not any_checked:
                QMessageBox.warning(self, "Not Checked", "Please select at least one checkbox to proceed.")
                return

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred during system hardening: {e}")

    def system(self):
        try:
            Id = subprocess.check_output(['systeminfo'], shell=True).decode('utf-8').split('\n')

            system_info = []
            for item in Id:
                if item.strip():
                    key_value = item.split(":", 1)
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        value = key_value[1].strip()
                        system_info.append((key, value))

            self.system_info.clearContents()
            self.system_info.setRowCount(len(system_info))

            for row, (key, value) in enumerate(system_info):
                self.system_info.setItem(row, 0, QTableWidgetItem(key))
                self.system_info.setItem(row, 1, QTableWidgetItem(value))

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to retrieve system information:\n{str(e)}")

    def __init__(self):

        super(MainWindow, self).__init__()
        self.setupUi(self)

        # button
        self.check_security_result.hide()
        self.hardening.hide()
        self.submit_hardening.hide()
        self.system()

        # section
        self.result_table.hide()
        self.dashboard_plot.hide()
        self.hardening_table.hide()

        # connect
        self.browse.clicked.connect(self.browse_file)
        self.submit.clicked.connect(self.path_extract)
        self.check_security.clicked.connect(self.registry_checking)
        self.cancel.clicked.connect(self.cancel_button)
        self.check_security_result.clicked.connect(self.dashboard)
        self.hardening.clicked.connect(self.table_hardening)
        self.submit_hardening.clicked.connect(self.system_hardening)

if __name__ == '__main__':

    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()
    splash.progress()

    ui = MainWindow()
    ui.show()

    splash.finish(ui)
    sys.exit(app.exec())