import tkinter as tk
from tkinter import ttk
from logger.serial_utils import *
from logger.SerialDataSource import SerialDataSource

# https://stackoverflow.com/a/30489525
class SerialCOM_Widget(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.SerialConfigFrame = self
        self.setup()

        self.DataSource = None
        self.DataSinkQueue = None

    def setup(self):
        """Calls methods to setup the user interface."""
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):

        ## SERIALCONFIGFRAME
        ### widgets
        self.cb_port = ttk.Combobox(self.SerialConfigFrame, values=serial_device_list())
        #self.cb_port.pack()
        self.cb_port.bind('<<ComboboxSelected>>', self.on_port_select)     # assign function to combobox
        self.cb_port.current(0)
        self.cb_baud = ttk.Combobox(self.SerialConfigFrame, values=serial_common_baud_rate_list())
        #self.cb_baud.pack()
        self.cb_baud.current(0)
        # https://stackoverflow.com/a/41189486
        self.cb_baud.bind('<<ComboboxSelected>>', self.on_baudrate_select)     # assign function to combobox

        self.btn_SerialConnect_text = tk.StringVar()   # state that will change
        self.btn_SerialConnect_text.set("Open")
        self.btn_SerialConnect = ttk.Button(self.SerialConfigFrame, textvariable=self.btn_SerialConnect_text,
                             command=self.on_btn_SerialConnect)

    def setup_layout(self):

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(column=0, row=0, columnspan=5, sticky="nesw")
        self.SerialConfigFrame.grid_rowconfigure(2, weight=1)
        self.cb_port.grid(column=0, row=0, columnspan=2)
        self.cb_baud.grid(column=2, row=0, columnspan=2)
        self.btn_SerialConnect.grid(column=4, row=0)

    ## SERIALCONFIGFRAME
    def on_port_select(self,event=None):
        #print("event.widget:", event.widget.get())
        print("comboboxes: ", self.cb_port.get())

    def on_baudrate_select(self,event=None):
        #print("event.widget:", event.widget.get())
        print("comboboxes: ", self.cb_baud.get())

    def on_btn_SerialConnect(self):
        print("button state:", self.btn_SerialConnect_text.get())
        if  self.btn_SerialConnect_text.get() == "Open":
            # if successful allow us to close the serial...
            self.DataSource = SerialDataSource(self.cb_port.get(), self.cb_baud.get())
            self.btn_SerialConnect_text.set("Close")
            self.DataSource.start()
        else:
            self.DataSource.stop()
            self.DataSource = None
            self.btn_SerialConnect_text.set("Open")


if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("480x300")
    SerialCOM_Widget(root)
    root.mainloop()