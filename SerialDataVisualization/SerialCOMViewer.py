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
from SerialDataVisualization.LoggerWindow import LoggerWindow
from SerialDataVisualization.PlotterWindow import PlotterWindow
from SerialDataVisualization.Visualization3DWindow import Visualization3DWindow
from SerialDataVisualization.SerialCOM_Rx_Widget import SerialCOM_Rx_Widget
import configparser
import time


class SerialCOMViewer(tk.Tk):  # a tk.Toplevel
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("SerialCOMViewer")
        self.root = self
        self.setup()

        # TODO: dictionary<key=type, val=list>
        self.PlotWindowList = []
        self.LogWindowList= []
        self.VisOrientList = []
        self.VisVectorList = []
        self.DataSource = None
        self.DataSinkQueue = None
        self.run_data_view = False
        self.after_id = 0
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def __del__(self):
        self.quit()

    def add_to_config(self, section):
        section['Serial'] = {}
        self.SerialCOM_Rx.add_to_config(section['Serial'])
        index = 0
        for i in self.PlotWindowList:
            if i.run: # check if window is alive
                section['Plotter'+str(index)] = {}
                i.add_to_config(section['Plotter'+str(index)])
                index += 1
        index = 0
        for i in self.LogWindowList:
            if i.run:  # check if window is alive
                section['Logger'+str(index)] = {}
                i.add_to_config(section['Logger'+str(index)])
                index += 1
        index = 0
        for i in self.VisVectorList:
            if i.run:  # check if window is alive
                section['VisVector'+str(index)] = {}
                i.add_to_config(section['VisVector'+str(index)])
                index += 1
        index = 0
        for i in self.VisOrientList:
            if i.run:  # check if window is alive
                section['VisOrient'+str(index)] = {}
                i.add_to_config(section['VisOrient'+str(index)])
                index += 1


    def load_from_config(self, section):
        self.SerialCOM_Rx.load_from_config(section['Serial'])
        self.SerialCOM_Rx.on_btn_SerialConnect()

        for key in section:
            print(key)
            if key.find('Plotter') > -1:
                w = self.on_btn_CreatePlotter()
                w.load_from_config(section[key])
                w.on_btn_Create()

            if key.find('Logger') > -1:
                w = self.on_btn_CreateLogger()
                w.load_from_config(section[key])
                w.on_btn_Create()
            if key.find('VisVector') > -1:
                w = self.on_btn_CreateVisVector()
                w.load_from_config(section[key])
                w.on_btn_Create()
            if key.find('VisOrient') > -1:
                w = self.on_btn_CreateVisOrient()
                w.load_from_config(section[key])
                w.on_btn_Create()
        print('loading config section done!')

    def close_window(self):
        self.SerialCOM_Rx.close_window()
        for i in self.PlotWindowList:
            if i.run:
                i.close_window()

        for i in self.LogWindowList:
            if i.run:
                i.close_window()

        time.sleep(0.1)
        self.destroy()

    def setup(self):
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
        self.btn_CreateVisOrient_text = tk.StringVar()   # state that will change
        self.btn_CreateVisOrient_text.set("Orientation Visualization")
        self.btn_CreateVisOrient = ttk.Button(self.LoggerConfigFrame, textvariable=self.btn_CreateVisOrient_text,
                             command=self.on_btn_CreateVisOrient)
        self.btn_CreateVisVector_text = tk.StringVar()   # state that will change
        self.btn_CreateVisVector_text.set("Vector Visualization")
        self.btn_CreateVisVector = ttk.Button(self.LoggerConfigFrame, textvariable=self.btn_CreateVisVector_text,
                             command=self.on_btn_CreateVisVector)

    def setup_layout(self):
        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(column=0, row=0, columnspan=5, sticky="nesw")
        ## LOGGERCONFIGFRAME:
        self.LoggerConfigFrame.grid(column=0, row=1, columnspan=5, sticky="nesw")
        self.btn_CreatePlotter.grid(column=1, row=1, columnspan=2)
        self.btn_CreateLogger.grid(column=3, row=1, columnspan=2)
        self.btn_CreateVisOrient.grid(column=1, row=2, columnspan=2)
        self.btn_CreateVisVector.grid(column=3, row=2, columnspan=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        return



    def OpenFile(self):
        filename = askopenfilename(title = "Select Config file", filetypes = (("ini files","*.ini"),("all files","*.*")))
        print(filename)
        config = configparser.ConfigParser()
        config.read(filename)
        print('Load config file....')
        self.load_from_config(config)

    def SaveAs(self):
        filename = asksaveasfilename(title = "Select Config file", filetypes = (("ini files","*.ini"),("all files","*.*")))
        print(filename)
        config = configparser.ConfigParser()

        self.add_to_config(config)
        print('Save config file....')
        with open(filename, 'w') as configfile:
            config.write(configfile)
            configfile.close()

    ## HELPMENU
    def About(self):
        print("Please check the readme")


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
            return w


    def on_btn_CreatePlotter(self):
        data_source = self.get_IDataSource()
        if data_source is not None:
            w = PlotterWindow(self)
            w.Source = data_source
            self.PlotWindowList.append(w)
            return w

    def on_btn_CreateVisOrient(self):
        data_source = self.get_IDataSource()
        if data_source is not None:
            w = Visualization3DWindow(self, type="orientation")
            w.Source = data_source
            self.VisOrientList.append(w)
            return w

    def on_btn_CreateVisVector(self):
        data_source = self.get_IDataSource()
        if data_source is not None:
            w = Visualization3DWindow(self, type="vector")
            w.Source = data_source
            self.VisVectorList.append(w)
            return w


if __name__ == '__main__':
    app = SerialCOMViewer()
    app.geometry("480x720")
    app.mainloop()