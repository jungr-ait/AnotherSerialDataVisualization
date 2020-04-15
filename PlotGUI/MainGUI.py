####
# https://github.com/furas/python-examples/blob/master/tkinter/matplotlib-canvas/main-minimal-navigationbar.py
# https://tkdocs.com/tutorial/widgets.html
# https://www.python-course.eu/tkinter_buttons.php
# https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-entry/
# https://www.programcreek.com/python/example/104110/tkinter.ttk.Combobox

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from logger.serial_utils import *
from logger.SerialDataSource import SerialDataSource
from logger.DataSinkQueue import DataSinkQueue
from PlotGUI.LoggerWindow import LoggerWindow
from PlotGUI.PlotterWindow import PlotterWindow

class MainGUI(tk.Tk):  # a tk.Toplevel
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("MainGUI")
        self.root = self
        #self.ContentFrame = ttk.Frame(self, padding=(3, 3, 12, 12))
        #self.ContentFrame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.setup()

        self.PlotWindowList = []
        self.LogWindowList= []
        self.DataSource = None
        self.DataSinkQueue = None
        self.run_data_view = False
        self.after_id = 0

    def __del__(self):
        self.run_data_view = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        self.quit()

    def setup(self):
        """Calls methods to setup the user interface."""
        self.init_menu()
        self.create_widgets()
        self.setup_layout()

    def init_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        ## FILEMENU
        filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.OpenFile)
        filemenu.add_command(label="Save as...", command=self.SaveAs)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        ## HELPMENU
        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)


    def create_widgets(self):

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame = tk.ttk.Labelframe(self, text='SerialConfig', padding=15)
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

        ## LOGGERCONFIGFRAME:
        self.LoggerConfigFrame = tk.ttk.Labelframe(self, text='LoggerConfig', padding=15)
        ### widgets
        self.btn_CreatePlotter_text = tk.StringVar()   # state that will change
        self.btn_CreatePlotter_text.set("Plotter Window")
        self.btn_CreatePlotter = ttk.Button(self.LoggerConfigFrame, textvariable=self.btn_CreatePlotter_text,
                             command=self.on_btn_CreatePlotter)
        self.btn_CreateLogger_text = tk.StringVar()   # state that will change
        self.btn_CreateLogger_text.set("Logger Window")
        self.btn_CreateLogger = ttk.Button(self.LoggerConfigFrame, textvariable=self.btn_CreateLogger_text,
                             command=self.on_btn_CreateLogger)


        ## DATAVIEWGFRAME:
        self.DataViewFrame = ttk.Labelframe(self, text='DataView', padding=15)
        ### widgets
        self.lst_DataView = tk.Listbox(self.DataViewFrame)
        self.scrl_DataView = ttk.Scrollbar(self.DataViewFrame, orient=tk.VERTICAL, command=self.lst_DataView.yview)
        self.lst_DataView['yscrollcommand'] = self.scrl_DataView.set
        self.lst_DataView.insert('end', 'empty...')
        self.lst_DataView.size()
        self.lst_DataView_buffersize  = 50 # max buffersize in listbox.
        self.btn_DataViewClear = ttk.Button(self.DataViewFrame, text='Clear',
                             command=self.delete_dataview)


    def setup_layout(self):

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(column=0, row=0, columnspan=5, sticky="nesw")
        self.SerialConfigFrame.grid_rowconfigure(2, weight=1)
        self.cb_port.grid(column=0, row=0, columnspan=2)
        self.cb_baud.grid(column=2, row=0, columnspan=2)
        self.btn_SerialConnect.grid(column=4, row=0)

        ## LOGGERCONFIGFRAME:
        self.LoggerConfigFrame.grid(column=0, row=1, columnspan=5, sticky="nesw")
        self.btn_CreatePlotter.grid(column=1, row=1, columnspan=2)
        self.btn_CreateLogger.grid(column=3, row=1, columnspan=2)

        ## DATAVIEWGFRAME:
        self.DataViewFrame.grid(column=0, row=2, columnspan=5, sticky="nesw")
        self.DataViewFrame.grid_rowconfigure(2, weight=1)
        self.DataViewFrame.grid_columnconfigure(0, weight=1)
        self.lst_DataView.grid(column=0, row=2, sticky="nesw")
        self.scrl_DataView.grid(column=1, row=2, sticky="nesw")
        self.btn_DataViewClear.grid(column=0, row=3, sticky="nesw")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        return


    ## FILEMENU
    def client_exit(self):
        exit()

    def OpenFile(self):
        name = askopenfilename()
        print(name)

    def SaveAs(self):
        name = asksaveasfilename()
        print(name)

    ## HELPMENU
    def About(self):
        print("This is a simple example of a menu")

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
            self.DataSinkQueue = DataSinkQueue(len=1000)
            self.DataSource.add_sink(self.DataSinkQueue)
            self.run_data_view = True
            self.delete_dataview()  # clear content of data view
            self.refresh_plot()
            self.DataSource.start()
        else:
            self.run_data_view = False
            self.DataSource.remove_sink(self.DataSinkQueue)
            self.DataSinkQueue = None
            self.DataSource.stop()
            self.DataSource = None
            self.btn_SerialConnect_text.set("Open")


    def get_IDataSource(self):
        if self.DataSource is None:
            tk.messagebox.showerror("Open Serial", message="First we need a IDataSource!")

        return self.DataSource

    ## LOGGERCONFIGFRAME:
    def on_btn_CreateLogger(self):
        data_source = self.get_IDataSource()
        if data_source is not None:
            w = LoggerWindow(self)
            w.Source = self.DataSource


    def on_btn_CreatePlotter(self):
        data_source = self.get_IDataSource()
        data_source = self.get_IDataSource()
        if data_source is not None:
            w = PlotterWindow(self)
            w.Source = self.DataSource


    ## DATAVIEWGFRAME:
    def delete_dataview(self):
        self.lst_DataView.delete(0, self.lst_DataView.size())


    ## from DataFormatParser
    def parse_line(self, line):
        self.lst_DataView.insert('end', line)
        if self.lst_DataView.size() > self.lst_DataView_buffersize:
            self.lst_DataView.delete(0, self.lst_DataView.size()-self.lst_DataView_buffersize)


    def refresh_plot(self):
        #https://riptutorial.com/tkinter/example/22870/-after--
        if self.run_data_view:
            if self.DataSinkQueue is not None:
                while(self.DataSinkQueue.available()):
                    self.parse_line(self.DataSinkQueue.data_queue.get())


            self.after_id =self.after(100, self.refresh_plot)


    def stop(self):
        print("stop")


if __name__ == '__main__':
    app = MainGUI()
    app.geometry("480x720")
    app.mainloop()