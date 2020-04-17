import tkinter as tk
from tkinter import ttk
from PlotGUI.SerialCOM_Widget import SerialCOM_Widget

class SerialCOM_Rx_Widget(SerialCOM_Widget):
    def __init__(self, parent, *args, **kwargs):
        SerialCOM_Widget.__init__(self, parent, *args, **kwargs)
        
        ## RxDataViewFRAME:
        self.RxDataViewFrame = ttk.Labelframe(self, text='RxDataView', padding=15)
        ### widgets
        self.RxDataViewFrame_Upper = tk.Frame(self.RxDataViewFrame)
        self.lst_RxDataView = tk.Listbox(self.RxDataViewFrame_Upper)
        self.scrl_RxDataView = ttk.Scrollbar(self.RxDataViewFrame_Upper, orient=tk.VERTICAL,
                                             command=self.lst_RxDataView.yview)
        self.lst_RxDataView['yscrollcommand'] = self.scrl_RxDataView.set
        self.lst_RxDataView.insert('end', 'empty...')
        self.lst_RxDataView.size()
        self.lst_RxDataView_buffersize  = 50 # max buffersize in listbox.
        self.btn_RxDataViewClear = ttk.Button(self.RxDataViewFrame, text='Clear',
                             command=self.delete_RxDataView)

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(row=0, column=0 , columnspan=5)
        self.cb_port.grid(row=0, column=0, columnspan=2)
        self.cb_baud.grid(row=0, column=2, columnspan=2)
        self.btn_SerialConnect.grid(row=0, column=4)

        ## RxDataViewFRAME:
        self.RxDataViewFrame.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.lst_RxDataView.pack(side="left", fill="both", expand=True)
        self.scrl_RxDataView.pack(side="left", fill="y")
        self.RxDataViewFrame_Upper.pack(side="top", fill="both", expand=True)
        self.btn_RxDataViewClear.pack(side="top", fill="x", expand=True)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
    ## DATAVIEWGFRAME:
    def delete_RxDataView(self):
        self.lst_RxDataView.delete(0, self.lst_RxDataView.size())


if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("480x300")
    SerialCOM_Rx_Widget(root)
    root.mainloop()