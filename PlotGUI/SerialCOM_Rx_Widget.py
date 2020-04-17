import tkinter as tk
from tkinter import ttk
from PlotGUI.SerialCOM_Widget import SerialCOM_Widget
from PlotGUI.YScrollListbox_Widget import YScrollListbox_Widget
from logger.DataSinkQueue import DataSinkQueue

class SerialCOM_Rx_Widget(SerialCOM_Widget):
    def __init__(self, parent, refresh_rate_ms=100, *args, **kwargs):
        SerialCOM_Widget.__init__(self, parent, *args, **kwargs)
        self.DataSink = DataSinkQueue()
        self.refresh_rate_ms = refresh_rate_ms
        self.refresh_view = False
        self.after_id = 0

        ## RxDataViewFRAME:
        self.RxDataViewFrame = ttk.Labelframe(self, text='RxDataView', padding=5)
        ### widgets
        self.YScrollListbox = YScrollListbox_Widget(self.RxDataViewFrame, buffer_size=50)
        self.LowerFrame = tk.Frame(self.RxDataViewFrame)
        self.btn_RxDataViewClear = ttk.Button(self.LowerFrame, text='Clear',
                             command=self.on_delete_RxDataView)

        self.btn_RxDataViewPause_text = tk.StringVar()  # state that will change
        self.btn_RxDataViewPause_text.set('Pause')
        self.btn_RxDataViewPause = ttk.Button(self.LowerFrame, textvariable=self.btn_RxDataViewPause_text,
                             command=self.on_delete_RxDataView)


        ## SERIALCONFIGFRAME
        self.SerialConfigFrame.grid(row=0, column=0 , columnspan=5)
        self.cb_port.grid(row=0, column=0, columnspan=2)
        self.cb_baud.grid(row=0, column=2, columnspan=2)
        self.btn_SerialConnect.grid(row=0, column=4)

        ## RxDataViewFRAME:
        self.RxDataViewFrame.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.YScrollListbox.pack(side="top", fill="both", expand=True)
        self.LowerFrame.pack(side="top", fill="x", expand=True)
        self.btn_RxDataViewClear.pack(side="left", fill="x", expand=True)
        self.btn_RxDataViewPause.pack(side="left", fill="x", expand=True)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)


    def __del__(self):
        self.refresh_view = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        self.quit()


    ## DATAVIEWGFRAME:
    def on_delete_RxDataView(self):
        self.YScrollListbox.clear_listbox()

    def on_pause_RxDataView(self):
        if self.btn_RxDataViewPause_text.get() == 'Pause':
            self.refresh_view = False
            self.btn_RxDataViewPause_text.set('Continue')
        else: # 'Continue'
            self.btn_RxDataViewPause_text.set('Pause')
            self.refresh_view = True


    def refresh(self):
        #https://riptutorial.com/tkinter/example/22870/-after--
        if (self.refresh_view) & (self.DataSink is not None):
            while self.DataSink.available():
                self.YScrollListbox.append_line(self.DataSink.data_queue.get())

            self.after_id = self.after(self.refresh_rate_ms, self.refresh)


    def serial_port_opened(self):
        self.on_delete_RxDataView()
        self.refresh_view = True
        self.DataSource.add_sink(self.DataSink)
        self.refresh()


    def serial_port_closed(self):
        self.DataSource.remove_sink(self.DataSink)




if __name__ == "__main__":
    root = tk.Tk()
    root.title('SerialCOM_Rx_Widget - Test')
    SerialCOM_Rx_Widget(root)
    root.mainloop()