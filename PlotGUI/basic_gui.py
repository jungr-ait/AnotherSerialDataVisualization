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
from logger.serial_utils import *



class MainGUI(tk.Tk):  # a tk.Toplevel
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("MainGUI")
        self.root = self
        #self.ContentFrame = ttk.Frame(self, padding=(3, 3, 12, 12))
        #self.ContentFrame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.setup()

        self.PlotWindowList = [];


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
        filemenu.add_command(label="New", command=self.NewFile)
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
        self.lbl_LoggerFormat = ttk.Label(self.LoggerConfigFrame, text="LoggerFormat:")
        self.txtvar_LoggerFormatusername = tk.StringVar()
        self.txtvar_LoggerFormatusername.set('%f,%f,%f')
        self.txt_LoggerFormat = ttk.Entry(self.LoggerConfigFrame, textvariable=self.txtvar_LoggerFormatusername)
        self.btn_CreatePlotter_text = tk.StringVar()   # state that will change
        self.btn_CreatePlotter_text.set("Create Plotter")
        self.btn_CreatePlotter = ttk.Button(self.LoggerConfigFrame, textvariable=self.btn_CreatePlotter_text,
                             command=self.on_btn_CreatePlotter)
        self.btn_CreateLogger_text = tk.StringVar()   # state that will change
        self.btn_CreateLogger_text.set("Create Logger")
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
        for i in range(1, 101):
            self.add_line_to_dataview('Line %d of 100' % i)


    def setup_layout(self):

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(column=0, row=0, columnspan=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.SerialConfigFrame.grid_rowconfigure(2, weight=1)
        self.cb_port.grid(column=0, row=0, columnspan=2)
        self.cb_baud.grid(column=2, row=0, columnspan=2)
        self.btn_SerialConnect.grid(column=4, row=0)

        ## LOGGERCONFIGFRAME:
        self.LoggerConfigFrame.grid(column=0, row=1, columnspan=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.LoggerConfigFrame.grid_rowconfigure(2, weight=1)
        self.lbl_LoggerFormat.grid(column=0, row=1, columnspan=2, sticky=(tk.E))
        self.txt_LoggerFormat.grid(column=2, row=1, columnspan=2)
        self.btn_CreatePlotter.grid(column=4, row=1)
        self.btn_CreateLogger.grid(column=5, row=1)

        ## DATAVIEWGFRAME:
        self.DataViewFrame.grid(column=0, row=2, columnspan=5, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.DataViewFrame.grid_rowconfigure(2, weight=1)
        self.DataViewFrame.grid_columnconfigure(0, weight=1)
        self.lst_DataView.grid(column=0, row=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.scrl_DataView.grid(column=1, row=2, sticky=(tk.N, tk.S, tk.E))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)
        # self.columnconfigure(3, weight=1)
        # self.columnconfigure(4, weight=1)

        return


    ## FILEMENU
    def client_exit(self):
        exit()

    def NewFile(self):
        print("New File!")

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

            self.btn_SerialConnect_text.set("Close")
        else:
            self.btn_SerialConnect_text.set("Open")

    ## LOGGERCONFIGFRAME:
    def on_btn_CreatePlotter(self):
        print("button state:", self.btn_CreatePlotter_text.get())

    def on_btn_CreateLogger(self):
        print("button state:", self.btn_CreateLogger_text.get())



    ## DATAVIEWGFRAME:
    def delete_dataview(self):
        self.lst_DataView.delete(0, self.lst_DataView.size())

    def add_line_to_dataview(self, line):
        print("add line to lst_DataView...")
        self.lst_DataView.insert('end', line)
        if self.lst_DataView.size() > self.lst_DataView_buffersize:
            self.lst_DataView.delete(0, 10)
            print("delete items from lst_DataView...")



if __name__ == '__main__':
    app = MainGUI()
    app.geometry("1280x720")
    app.mainloop()