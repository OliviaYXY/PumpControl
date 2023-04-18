

import sys
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QCheckBox, QTextEdit
import serial
import time
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QRect


class PumpControlApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.port_label = QLabel('Port:', self)
        self.port_label.move(20, 20)
        self.port_text = QLineEdit(self)
        self.port_text.move(80, 20)
        self.port_text.setText('COM1')
        self.baud_rate_label = QLabel('Baud Rate:', self)
        self.baud_rate_label.move(20, 60)
        self.baud_rate_text = QLineEdit(self)
        self.baud_rate_text.move(80, 60)
        self.baud_rate_text.setText('9600')
        self.connect_button = QPushButton('Connect', self)
        self.connect_button.move(20, 100)
        self.connect_button.clicked.connect(self.connect_to_pump_control_station)
        self.disconnect_button = QPushButton('Disconnect', self)
        self.disconnect_button.move(120, 100)
        self.disconnect_button.clicked.connect(self.disconnect_from_pump_control_station)
        self.status_label = QLabel('Not connected', self)
        self.status_label.move(20, 140)
        self.status_label.setMinimumWidth(150)

        # Create checkbox for selecting all rows
        self.select_all_checkbox = QCheckBox('Select All', self)
        self.select_all_checkbox.move(180, 140)
        self.select_all_checkbox.stateChanged.connect(self.select_all_rows)

        # Set total pump number
        #self.pump_number_text = QLabel('Total Pump Number:', self)
        #self.pump_number_text.move(220, 20)
        #self.pump_number_text = QLineEdit(self)
        #self.pump_number_text.move(340, 20)
        #self.pump_number_text.setText('2')

        # Create table widget
        self.pump_table = QTableWidget(self)
        self.pump_table.move(20, 180)
        self.pump_table.setRowCount(8)
        self.pump_table.setColumnCount(7)
        self.pump_table.setHorizontalHeaderLabels(
            ['', 'Number', 'Content', 'Diameter(mm)', 'Flow Rate(ul/h)', 'Condition', 'Remarks'])
        self.pump_table.horizontalHeader().setStretchLastSection(True)
        self.pump_table.setColumnWidth(0, 30)
        self.pump_table.setColumnWidth(1, 100)
        self.pump_table.setColumnWidth(2, 100)
        self.pump_table.setColumnWidth(3, 100)
        self.pump_table.setColumnWidth(4, 100)
        self.pump_table.setColumnWidth(5, 100)
        self.pump_table.setColumnWidth(6, 150)

        # Set checkbox in the first column of each row
        for i in range(self.pump_table.rowCount()):
            checkbox = QCheckBox()
            self.pump_table.setCellWidget(i, 0, checkbox)

        # Create the Set button
        self.set_button = QPushButton('Set Select', self)
        self.set_button.move(300, 140)
        self.set_button.clicked.connect(self.on_set_button_clicked)
        self.set_button.setStyleSheet("background-color:#ffd460")

        # Create the Refresh button
        self.Refresh_button = QPushButton('Refresh Select', self)
        self.Refresh_button.move(420, 140)
        self.Refresh_button.setStyleSheet("background-color:#f07b3f")
        self.Refresh_button.clicked.connect(self.on_refresh_button_clicked)

        # Create the Run select button
        self.Run_button = QPushButton('Run Select', self)
        self.Run_button.move(540, 140)
        self.Run_button.setStyleSheet("background-color:#ea5455")
        self.Run_button.clicked.connect(self.on_run_select_button_clicked)

        # Create the Stop select button
        self.Stop_button = QPushButton('Stop Select', self)
        self.Stop_button.move(660, 140)
        self.Stop_button.setStyleSheet("background-color:#2d4059")
        self.Stop_button.clicked.connect(self.on_stop_select_button_clicked)

        # Set main window properties
        self.setGeometry(100, 100, 800, 500)
        self.setWindowTitle('Pump Control Station')

    def select_all_rows(self, state):
        for i in range(self.pump_table.rowCount()):
            checkbox = self.pump_table.cellWidget(i, 0)
            checkbox.setChecked(state == Qt.Checked)

    def connect_to_pump_control_station(self):
        try:
            # Connect to modbus RTU
            self.master = modbus_rtu.RtuMaster(
                serial.Serial(port=self.port_text.text(), baudrate=int(self.baud_rate_text.text()), bytesize=8,
                                                                       parity='E', stopbits=1)
            )
            self.master.set_timeout(5.0)
            self.master.set_verbose(True)
            # read = self.master.execute(1, cst.READ_HOLDING_REGISTERS, 10, 2)

            # Update status label
            self.status_label.setText('Connected')

            # TODO: Add code to update UI based on pump control station values

            # Add sample data to pump table
            for row in range(self.pump_table.rowCount()):
                self.pump_table.setItem(row, 1, QTableWidgetItem(str(row+1)))
                self.pump_table.setItem(row, 3, QTableWidgetItem('4.7'))
                self.pump_table.setItem(row, 4, QTableWidgetItem('200.00'))
                self.pump_table.setItem(row, 5, QTableWidgetItem('Stopped'))

            #self.pump_table.setItem(0, 1, QTableWidgetItem('1'))
            self.pump_table.setItem(0, 2, QTableWidgetItem('Water'))
            self.pump_table.setItem(0, 5, QTableWidgetItem('Stopped'))
            self.pump_table.setItem(0, 6, QTableWidgetItem('Sample'))
            #self.pump_table.setItem(1, 1, QTableWidgetItem('2'))
            self.pump_table.setItem(1, 2, QTableWidgetItem('Oil'))
            #self.pump_table.setItem(1, 3, QTableWidgetItem('4.7'))
            self.pump_table.setItem(1, 4, QTableWidgetItem('800.00'))
            self.pump_table.setItem(1, 5, QTableWidgetItem('Stopped'))
            self.pump_table.setItem(1, 6, QTableWidgetItem('Sample'))

            # Set checkbox in the first column of each row
            for i in range(self.pump_table.rowCount()):
                checkbox = QCheckBox()
                self.pump_table.setCellWidget(i, 0, checkbox)

        except Exception as e:
            print('Failed to connect to pump control station:', e)
            self.status_label.setText('Connection failed')


    def disconnect_from_pump_control_station(self):
            # Close modbus RTU connection
            self.master.close()

            # Update status label
            self.status_label.setText('Not connected')

            # Clear pump table
            self.pump_table.clearContents()

    def resizeEvent(self, event):
        # Resize pump table widget to fit window
        table_width = self.width() - 40
        table_height = self.height() - 200
        self.pump_table.setFixedSize(table_width, table_height)

    def on_set_button_clicked(self):
        # This function will be called when the "Set" button is clicked
        for row in range(self.pump_table.rowCount()):
            checkbox = self.pump_table.cellWidget(row, 0)
            if checkbox.isChecked():
                number = int(self.pump_table.item(row, 1).text())
                # Set default time (1 hour)
                pump_add = int(number) * 1000 + 12
                set_time = 60 * 60
                # print("type of time after", type([time])) # 'list'
                self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, pump_add, output_value=[set_time],
                                    data_format='>f')
                print("Pump ", number, "running time has been set to", set_time / 3600, "hour")
                print(row)
                time.sleep(0.1)

                diameter = float(self.pump_table.item(row, 3).text())
                k = (diameter / 4.7) ** 2
                flow_rate = float(self.pump_table.item(row, 4).text())/k
                #print("flow_rate", flow_rate)
                q_address = int(number) * 1000 + 10
                self.master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, q_address, output_value=[flow_rate],
                                    data_format='>f')
                print("Pump ", number, "volume has been set to ", flow_rate, "ul/h.")
                time.sleep(0.1)

    def on_refresh_button_clicked(self):
        # This function will be called when the "Refresh" button is clicked
        for row in range(self.pump_table.rowCount()):
            checkbox = self.pump_table.cellWidget(row, 0)
            if checkbox.isChecked():
                number = int(self.pump_table.item(row, 1).text())
                diameter = float(self.pump_table.item(row, 3).text())
                k = (diameter / 4.7) ** 2
                q_address = number * 1000 + 10
                now_flow_rate = self.master.execute(1, cst.READ_HOLDING_REGISTERS, q_address, 2, data_format='>f') # 'tuple'
                #print(now_flow_rate[0])
                #print(type(now_flow_rate[0])) # 'tuple'
                k_now_flow_rate = now_flow_rate[0] * k
                self.pump_table.setItem(row, 4, QTableWidgetItem(str(k_now_flow_rate)))
                print("Pump ", number, "flow rate is ", k_now_flow_rate, "ul/h now.")
                time.sleep(0.1)

                con_address = number * 1000 + 3
                con = self.master.execute(1, cst.READ_HOLDING_REGISTERS, con_address, 1)
                time.sleep(0.1)
                #print(con)
                #print(type(con))
                if con[0] == 0:
                    self.pump_table.setItem(row, 5, QTableWidgetItem('Stopped'))
                    print("Pump ", number, "is stopped now.")
                if con[0] == 1:
                    self.pump_table.setItem(row, 5, QTableWidgetItem('Running'))
                    print("Pump ", number, "is running now.")
                time.sleep(0.1)


    def on_run_select_button_clicked(self):
        # This function will be called when the "Run-select" button is clicked
        for row in range(self.pump_table.rowCount()):
            checkbox = self.pump_table.cellWidget(row, 0)
            if checkbox.isChecked():
                # Write 1 to single register at the address of Number * 1000 + 3
                number = int(self.pump_table.item(row, 1).text())
                self.master.execute(1, cst.WRITE_SINGLE_REGISTER, number * 1000 + 3, output_value=1)
                self.pump_table.setItem(row, 5, QTableWidgetItem('Running'))
                print("Pump ", number, "is running.")
                time.sleep(0.1)

    def on_stop_select_button_clicked(self):
        # This function will be called when the "Set" button is clicked
        for row in range(self.pump_table.rowCount()):
            checkbox = self.pump_table.cellWidget(row, 0)
            if checkbox.isChecked():
                # Write 0 to single register at the address of Number * 1000 + 3
                number = int(self.pump_table.item(row, 1).text())
                self.master.execute(1, cst.WRITE_SINGLE_REGISTER, number * 1000 + 3, output_value=0)
                self.pump_table.setItem(row, 5, QTableWidgetItem('Stopped'))
                print("Pump ", number, "is stopped.")
                time.sleep(0.1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    pump_control_app = PumpControlApp()
    pump_control_app.show()
    sys.exit(app.exec_())

