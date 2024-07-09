import tkinter as tk
import tkinter.ttk as ttk
import time
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from SerialDataVisualization.PlotterModel import PlotterModel
from SerialDataVisualization.InfoWindow import InfoWindow
from SourceSink.IDataSource import IDataSource
from SourceSink.DataSinkQueue import DataSinkQueue
from SourceSink.VectorPlot3D import VectorPlot3D
from SourceSink.OrientationPlot import OrientationPlot
import configparser


class Visualization3DWindow(tk.Toplevel):
    Source = None
    def __init__(self, parent, source=None, title= "Visualization3DWindow!", type="vector"):
        tk.Toplevel.__init__(self, parent)  # instead of super
        self.title(title)
        self.type = type
        self.vis = None
        self.Source = source
        self.after_id = None
        self.run = True
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.setup()

    def add_to_config(self, section):
        fmt = self.txtvar_Format.get().replace('%', '%%')
        section['format_str'] = fmt
        section['title'] = self.txtvar_Title.get()
        section['interval_ms'] = str( self.cb_UpdateInterval.get())
        section['max_samples'] = str(self.cb_MaxSample.get())
        section['use_timestamp'] = str(self.checkvar_usetimestamp.get())

    def load_from_config(self, section):
        fmt = section.get('format_str', '%%f,%%f,%%f')
        self.txtvar_Format.set(fmt.replace('%%', '%'))
        self.txtvar_Title.set(section.get('title', 'no title'))
        self.cb_MaxSample.set(int(section.get('max_samples', '100')))
        self.cb_UpdateInterval.set(int(section.get('interval_ms', '100')))
        self.checkvar_usetimestamp.set(section.getboolean('use_timestamp', fallback=True))

    def close_window(self):

        self.run = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        time.sleep(0.1)
        self.destroy()


    def setup(self):
        self.init_menu()
        self.create_widgets()
        self.setup_layout()

    def init_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        ## HELPMENU
        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.on_About)
        helpmenu.add_command(label="Exit", command=self.destroy)

    def create_widgets(self):
        ## MainFrame:
        self.MainFrame = tk.ttk.Frame(self, padding=(10,5))

        ### widgets
        self.lbl_Type = ttk.Label(self.MainFrame, text="Type:")
        self.lbl_TypeVar = ttk.Label(self.MainFrame, text=self.type)
        self.lbl_Format = ttk.Label(self.MainFrame, text="Format:")
        self.txtvar_Format = tk.StringVar()
        self.txtvar_Format.set('%f,%f,%f')
        self.txt_Format = ttk.Entry(self.MainFrame, textvariable=self.txtvar_Format)

        self.lbl_Title = ttk.Label(self.MainFrame, text="Title:")
        self.txtvar_Title  = tk.StringVar()
        self.txtvar_Title.set('')
        self.txt_Title  = ttk.Entry(self.MainFrame, textvariable=self.txtvar_Title)

        # update interval: drop down list
        self.lbl_UpdateInterval = ttk.Label(self.MainFrame, text="UpdateInterval [ms]:")
        self.cb_UpdateInterval = ttk.Combobox(self.MainFrame, values=[10, 50, 100, 500, 1000, 10000])
        self.cb_UpdateInterval.current(1)

        # max_sample: drop down list
        self.lbl_MaxSample = ttk.Label(self.MainFrame, text="Max Samples:")
        self.cb_MaxSample = ttk.Combobox(self.MainFrame, values=[50, 100, 500, 1000, 5000])
        self.cb_MaxSample.current(0)

        self.checkvar_usetimestamp = tk.BooleanVar()
        self.checkvar_usetimestamp.set(False)
        self.check_usetimestamp = ttk.Checkbutton(self.MainFrame, text="use timestamp", variable=self.checkvar_usetimestamp, onvalue=True)


        self.txtbtn_Create = tk.StringVar()   # state that will change from Create to Close
        self.txtbtn_Create.set("Create Vis.")
        self.btn_Create = ttk.Button(self.MainFrame, textvariable=self.txtbtn_Create,
                             command=self.on_btn_Create)
        self.txtbtn_Pause = tk.StringVar()   # state that will change from Create to Close
        self.txtbtn_Pause.set("Pause")
        self.btn_Pause = ttk.Button(self.MainFrame, textvariable=self.txtbtn_Pause,
                             command=self.on_btn_Pause)


        ## PlotFrame
        self.PlotFrame = ttk.Labelframe(self, text='PlotFrame', padding=15)
        self.PlotCanvas = tk.Canvas(self.PlotFrame)

    def setup_layout(self):
        print('setup layout...')
        self.MainFrame.grid(         column=0, row=0, sticky="nesw")
        self.lbl_Type.grid(          column=0, row=0, columnspan=1, sticky='e')
        self.lbl_TypeVar.grid(       column=1, row=0, columnspan=1, sticky='w')
        self.lbl_Format.grid(        column=0, row=1, columnspan=1, sticky='e')
        self.txt_Format.grid(        column=1, row=1, columnspan=1, sticky='w')
        self.check_usetimestamp.grid(column=2, row=1, columnspan=1, sticky='e')
        self.lbl_Title.grid(         column=0, row=2, columnspan=1, sticky='e')
        self.txt_Title.grid(         column=1, row=2, columnspan=1, sticky='w')
        self.lbl_MaxSample.grid(     column=0, row=3, columnspan=1, sticky='e')
        self.cb_MaxSample.grid(      column=1, row=3, columnspan=1, sticky='w')
        self.lbl_UpdateInterval.grid(column=0, row=4, columnspan=1, sticky='e')
        self.cb_UpdateInterval.grid( column=1, row=4, columnspan=1, sticky='w')
        self.btn_Pause.grid(         column=0, row=5, columnspan=1, sticky='e')
        self.btn_Create.grid(        column=1, row=5, columnspan=1, sticky='w')

        # Streches MainFrame over TopLevel... a bit counter-intuitive
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.MainFrame.rowconfigure(0, weight=1)
        self.MainFrame.rowconfigure(1, weight=1)
        self.MainFrame.rowconfigure(2, weight=1)
        self.MainFrame.rowconfigure(3, weight=1)
        self.MainFrame.rowconfigure(4, weight=1)
        self.MainFrame.rowconfigure(5, weight=1)

        self.MainFrame.columnconfigure(0, weight=3)
        self.MainFrame.columnconfigure(1, weight=1)
        self.MainFrame.columnconfigure(2, weight=3)

    def on_About(self):
        with open("PlotterWindowAbout.txt") as f:
            info_str = f.read()
            self.info_window = InfoWindow(self, str(info_str))



    def on_btn_Pause(self):
        print("button state:", self.txtbtn_Pause.get())
        if self.txtbtn_Pause.get() == "Pause":
            # user wants to Pause
            self.txtbtn_Pause.set("Resume")
        else:
            # user wants to Resume:
            self.txtbtn_Pause.set("Pause")
            self.refresh_plot()

    def on_btn_Create(self):
        print("button state:", self.txtbtn_Create.get())
        if  self.txtbtn_Create.get() == "Create Vis.":

            if self.type == "vector":
                self.vis = VectorPlot3D(title=self.txt_Title.get(),
                              format_str=self.txt_Format.get(),
                              max_samples=self.cb_MaxSample.get(),
                              use_timestamp = self.checkvar_usetimestamp.get())
            elif self.type == "orientation":
                self.vis = OrientationPlot(title=self.txt_Title.get(),
                              format_str=self.txt_Format.get(),
                              max_samples=self.cb_MaxSample.get(),
                              use_timestamp = self.checkvar_usetimestamp.get())
            else:
                print("unknown type: " + self.type)
                return
            if isinstance(self.Source, IDataSource):
                self.Source.add_sink(self.vis)
                self.after_id =self.after(int(self.cb_UpdateInterval.get()), self.refresh_plot)

            self.txtbtn_Create.set("Close Vis.") # toggle state

        else:
            # Close SourceSink:
            self.txtbtn_Create.set("Create Vis.")

            if isinstance(self.Source, IDataSource):
                self.Source.remove_sink(self.vis)
            if self.vis is not None:
                del self.vis
                self.vis = None

    def refresh_plot(self):
        #https://riptutorial.com/tkinter/example/22870/-after--
        if (self.txtbtn_Create.get() == "Close Vis.") & (self.txtbtn_Pause.get() == "Pause") & self.run:
            if self.vis is not None:
                self.vis.plot_figure()
            if self.run:
                self.after_id =self.after(int(self.cb_UpdateInterval.get()), self.refresh_plot)


if __name__ == '__main__':
    root = tk.Tk()  # first toplevel window
    root.title("Root")
    root.protocol
    root.geometry("100x100")
    w = Visualization3DWindow(root)


    from SourceSink.MockSource import MockSource

    w.Source = MockSource(rate_ms=100)
    w.Source.start()
    root.mainloop()
    print("root is dead")
    w.Source.stop()
    print("source is dead")