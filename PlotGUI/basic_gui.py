import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import serial.tools.list_ports
import serial.utilities.compatibility

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)


class MainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("BASIS GUI")
        self.root = self

        self.init_window()
        self.init_menu()

    def init_window(self):
        self.window = tk.Frame(self)
        self.window.pack(side="top", fill="both", expand=True)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.cb_port = ttk.Combobox(self, values=self.serial_ports())
        self.cb_port.pack()
        self.cb_port.bind('<<ComboboxSelected>>', self.on_port_select)     # assign function to combobox
        self.cb_port.current(0)
        self.cb_baud = ttk.Combobox(self, values=self.baud_rates())
        self.cb_baud.pack()
        self.cb_baud.current(0)
        self.cb_baud.bind('<<ComboboxSelected>>', self.on_baudrate_select)     # assign function to combobox

        self.btn_open_serial_text = tk.StringVar()
        self.btn_open_serial_text.set("Open")
        self.btn_open_serial = ttk.Button(self, textvariable=self.btn_open_serial_text,
                             command=self.on_open_serial)
        self.btn_open_serial.pack()


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
        filemenu.add_command(label="Exit", command=self.root.quit)

        ## HELPMENU
        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


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

    def About(self):
        print("This is a simple example of a menu")

    def serial_ports(self):
        device_list = []
        for d in serial.tools.list_ports.comports():
            device_list.append(d.device)
        return device_list

    def baud_rates(self):
        return ["9600", "14400", "19200", "38400", "57600", "115200", "128000", "230400", "256000", "500000", "1000000"]


    def on_port_select(self,event=None):
        # get selection from event
        print("event.widget:", event.widget.get())

        # or get selection directly from combobox
        print("comboboxes: ", self.cb_port.get())

    def on_baudrate_select(self,event=None):
        # get selection from event
        print("event.widget:", event.widget.get())

        # or get selection directly from combobox
        print("comboboxes: ", self.cb_baud.get())

    def on_open_serial(self):
        print("button state:", self.btn_open_serial_text.get())
        if  self.btn_open_serial_text.get() == "Open":
            self.btn_open_serial_text.set("Close")
        else:
            self.btn_open_serial_text.set("Open")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()


if __name__ == '__main__':
    app = MainGUI()
    app.geometry("1280x720")
    app.mainloop()