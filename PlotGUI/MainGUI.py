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
from PlotGUI.SerialCOM_Rx_Widget import SerialCOM_Rx_Widget
import time

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
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def __del__(self):
        self.quit()

    def close_window(self):
        self.SerialCOM_Rx.close_window()
        for i in self.PlotWindowList:
            i.close_window()

        for i in self.LogWindowList:
            continue

        time.sleep(0.1)
        self.destroy()

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
        filemenu.add_command(label="Exit", command=self.close_window)

        ## HELPMENU
        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)


    def create_widgets(self):

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame = tk.ttk.Labelframe(self, text='SerialConfig', padding=15)
        ### widgets
        self.SerialCOM_Rx = SerialCOM_Rx_Widget(self.SerialConfigFrame)

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


    def setup_layout(self):
        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(column=0, row=0, columnspan=5, sticky="nesw")
        ## LOGGERCONFIGFRAME:
        self.LoggerConfigFrame.grid(column=0, row=1, columnspan=5, sticky="nesw")
        self.btn_CreatePlotter.grid(column=1, row=1, columnspan=2)
        self.btn_CreateLogger.grid(column=3, row=1, columnspan=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        return



    def OpenFile(self):
        name = askopenfilename()
        print(name)

    def SaveAs(self):
        name = asksaveasfilename()
        print(name)

    ## HELPMENU
    def About(self):
        print("This is a simple example of a menu")



    def get_IDataSource(self):
        if self.SerialCOM_Rx.DataSource is None:
            tk.messagebox.showerror("Open Serial", message="First a connection is required!")


        return self.SerialCOM_Rx.DataSource

    ## LOGGERCONFIGFRAME:
    def on_btn_CreateLogger(self):
        data_source = self.get_IDataSource()
        if data_source is not None:
            w = LoggerWindow(self)
            w.Source = data_source
            self.LogWindowList.append(w)


    def on_btn_CreatePlotter(self):
        data_source = self.get_IDataSource()
        if data_source is not None:
            w = PlotterWindow(self)
            w.Source = data_source
            self.PlotWindowList.append(w)



if __name__ == '__main__':
    app = MainGUI()
    app.geometry("480x720")
    app.mainloop()