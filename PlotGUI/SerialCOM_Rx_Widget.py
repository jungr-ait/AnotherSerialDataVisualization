import tkinter as tk
from tkinter import ttk
from PlotGUI.SerialCOM_Widget import SerialCOM_Widget
from PlotGUI.YScrollListbox_Widget import YScrollListbox_Widget


class SerialCOM_Rx_Widget(SerialCOM_Widget):
    def __init__(self, parent, *args, **kwargs):
        SerialCOM_Widget.__init__(self, parent, *args, **kwargs)
        
        ## RxDataViewFRAME:
        self.RxDataViewFrame = ttk.Labelframe(self, text='RxDataView', padding=5)
        ### widgets
        self.YScrollListbox = YScrollListbox_Widget(self.RxDataViewFrame, buffer_size=50)
        self.btn_RxDataViewClear = ttk.Button(self.RxDataViewFrame, text='Clear',
                             command=self.delete_RxDataView)

        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(row=0, column=0 , columnspan=5)
        self.cb_port.grid(row=0, column=0, columnspan=2)
        self.cb_baud.grid(row=0, column=2, columnspan=2)
        self.btn_SerialConnect.grid(row=0, column=4)

        ## RxDataViewFRAME:
        self.RxDataViewFrame.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.YScrollListbox.pack(side="top", fill="both", expand=True)
        self.btn_RxDataViewClear.pack(side="top", fill="x", expand=True)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    ## DATAVIEWGFRAME:
    def delete_RxDataView(self):
        self.YScrollListbox.clear_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('SerialCOM_Rx_Widget - Test')
    SerialCOM_Rx_Widget(root)
    root.mainloop()