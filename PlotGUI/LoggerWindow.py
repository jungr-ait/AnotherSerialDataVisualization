import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PlotGUI.LoggerModel import LoggerModel
from logger.IDataSource import IDataSource

def create_textfield(parent, lbl_text, default_text):
    lbl = ttk.Label(parent, text=lbl_text)
    txtvar = tk.StringVar()
    txtvar.set(default_text)
    txtentry = ttk.Entry(parent, textvariable=txtvar)
    return [lbl, txtvar, txtentry]




class LoggerWindow(tk.Toplevel):
    Source = None

    def __init__(self, parent, source=None, title= "I am a WindowLogger!"):
        tk.Toplevel.__init__(self, parent)  # instead of super
        self.title(title)
        self.setup()
        self.parent = parent
        self.Model = LoggerModel(self)
        self.Source = source

        
    def setup(self):
        """Calls methods to setup the user interface."""
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        ## MainFrame:
        self.MainFrame = tk.ttk.Frame(self, padding=(10,5))

        ### widgets
        self.lbl_Format = ttk.Label(self.MainFrame, text="Format:")
        self.txtvar_Format = tk.StringVar()
        self.txtvar_Format.set('%f,%f,%f')
        self.txt_Format = ttk.Entry(self.MainFrame, textvariable=self.txtvar_Format)

        self.lbl_Header = ttk.Label(self.MainFrame, text="Header:")
        self.txtvar_Header  = tk.StringVar()
        self.txtvar_Header .set('x,y,z')
        self.txt_Header  = ttk.Entry(self.MainFrame, textvariable=self.txtvar_Header)

        self.lbl_Filename = ttk.Label(self.MainFrame, text="Filename:")
        self.txtvar_Filename = tk.StringVar()
        self.txtvar_Filename.set('log.csv')
        self.txt_Filename = ttk.Entry(self.MainFrame, textvariable=self.txtvar_Filename)
        self.btn_FindFile = ttk.Button(self.MainFrame, text="File", command=self.on_btn_FindFile)


        self.checkvar_flush = tk.BooleanVar()
        self.checkvar_flush.set(True)
        self.check_flush = ttk.Checkbutton(self.MainFrame, text="Flush", variable=self.checkvar_flush, onvalue=True)

        self.txtbtn_Create = tk.StringVar()   # state that will change from Create to Close
        self.txtbtn_Create.set("Create Logger")
        self.btn_Create = ttk.Button(self.MainFrame, textvariable=self.txtbtn_Create,
                             command=self.on_btn_Create)


    def setup_layout(self):
        print('setup layout...')


        self.MainFrame.grid(column=0, row=0, sticky="nesw")

        self.lbl_Format.grid(column=0, row=0, columnspan=1, sticky='e')
        self.txt_Format.grid(column=1, row=0, columnspan=1, sticky='w')
        self.lbl_Header.grid(column=0, row=1, columnspan=1, sticky='e')
        self.txt_Header.grid(column=1, row=1, columnspan=1, sticky='w')
        self.lbl_Filename.grid(column=0, row=2, columnspan=1, sticky='e')
        self.txt_Filename.grid(column=1, row=2, columnspan=1, sticky='w')
        self.btn_FindFile.grid(column=2, row=2, columnspan=1, sticky='w')
        self.check_flush.grid(column=0, row=3, columnspan=1, sticky='e')
        self.btn_Create.grid(column=1, row=3, columnspan=1, sticky='w')

        # Streches MainFrame over TopLevel... a bit counter-intuitive
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.MainFrame.rowconfigure(0, weight=1)
        self.MainFrame.rowconfigure(1, weight=1)
        self.MainFrame.rowconfigure(2, weight=1)
        self.MainFrame.rowconfigure(3, weight=3)
        self.MainFrame.columnconfigure(0, weight=2)
        self.MainFrame.columnconfigure(1, weight=1)
        self.MainFrame.columnconfigure(2, weight=2)

        pass

    def on_btn_FindFile(self):
        print("button find file:")
        filename = asksaveasfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
        if len(filename):
            self.txtvar_Filename.set(filename)



    def on_btn_Create(self):
        print("button state:", self.txtbtn_Create.get())
        if  self.txtbtn_Create.get() == "Create Logger":
            self.Model.create_logger(self.txt_Filename.get(), self.txt_Format.get(),
                                     self.txt_Header.get(), self.checkvar_flush.get())

            # TODO: give the object the parent.serial_handler!
            if isinstance(self.Source, IDataSource):
                self.Source.add_sink(self.Model.get_logger())

            self.txtbtn_Create.set("Close Logger")
        else: 
            # Close logger:
            self.txtbtn_Create.set("Create Logger")
            # TODO: remove the object from the parent.serial_handler!

            if isinstance(self.Source, IDataSource):
                self.Source.remove_sink(self.Model.get_logger())
            self.Model.close_logger()


if __name__ == '__main__':
    root = tk.Tk()  # first toplevel window
    root.title("Root")
    root.geometry("100x100")
    w = LoggerWindow(root)


    from logger.SerialDataHandler import SerialDataHandler

    w.Source = SerialDataHandler(port='/dev/ttyUSB0', baud_rate=115200, timeout=1)
    w.Source.start()
    root.mainloop()