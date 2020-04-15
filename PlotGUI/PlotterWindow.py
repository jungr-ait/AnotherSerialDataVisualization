import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PlotGUI.LoggerModel import LoggerModel
from logger.IDataSource import IDataSource



class PlotterWindow(tk.Toplevel):
    Source = None
    def __init__(self, parent, source=None, title= "I am a PlotterWindow!"):
        tk.Toplevel.__init__(self, parent)  # instead of super
        self.title(title)
        self.setup()

