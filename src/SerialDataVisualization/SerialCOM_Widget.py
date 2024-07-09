import tkinter as tk
from tkinter import ttk
from SourceSink.serial_utils import *
from SourceSink.SerialDataSource import SerialDataSource
from tkinter.messagebox import showerror
import configparser

# https://stackoverflow.com/a/30489525
class SerialCOM_Widget(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.SerialConfigFrame = self
        self.DataSource = None

        ## SERIALCONFIGFRAME
        ### widgets
        self.cb_port = ttk.Combobox(self.SerialConfigFrame, values=serial_device_list())
        self.cb_port.current(0)
        self.cb_baud = ttk.Combobox(self.SerialConfigFrame, values=serial_common_baud_rate_list())
        self.cb_baud.current(0)

        self.btn_SerialConnect_text = tk.StringVar()  # state that will change
        self.btn_SerialConnect_text.set("Open")
        self.btn_SerialConnect = ttk.Button(self.SerialConfigFrame, textvariable=self.btn_SerialConnect_text,
                                            command=self.on_btn_SerialConnect)

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(row=0, column=0 , columnspan=5, sticky="nesw")
        self.SerialConfigFrame.grid_rowconfigure(2, weight=1)
        self.cb_port.grid(row=0, column=0, columnspan=2)
        self.cb_baud.grid(row=0, column=2, columnspan=2)
        self.btn_SerialConnect.grid(row=0, column=4)

    def add_to_config(self, section):
        section['device'] = str(self.cb_port.get())
        section['baud_rate'] = str(self.cb_baud.get())

    def load_from_config(self, section):
        self.cb_port.set(section.get('device', '/dev/ttyUSB0'))
        self.cb_baud.set(section.get('baud_rate', '115200'))


    def on_btn_SerialConnect(self):
        if  self.btn_SerialConnect_text.get() == "Open":
            if self.open_serial():
                self.btn_SerialConnect_text.set("Close")
        else:
            self.close_serial()
            self.btn_SerialConnect_text.set("Open")


    def open_serial(self):
        try:
            self.DataSource = SerialDataSource(self.cb_port.get(), self.cb_baud.get())
            self.DataSource.start()
            self.serial_port_opened()
            return True
        except Exception as e:
            print('open serial: ' + str(e))
            showerror(title="Error", message="Invalid serial port configuration")
            return False


    def close_serial(self):
        if self.DataSource is not None:
            self.DataSource.stop()
            self.serial_port_closed()
            self.DataSource = None


    def serial_port_opened(self):
        pass  # hook for child classes


    def serial_port_closed(self):
        pass  # hook for child classes



if __name__ == "__main__":
    root = tk.Tk()
    root.title('SerialCOM_Widget - Test')
    SerialCOM_Widget(root)
    root.mainloop()