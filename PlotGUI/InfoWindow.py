import tkinter as tk
import tkinter.ttk as ttk
import textwrap


class InfoWindow(tk.Toplevel):
    Source = None
    def __init__(self, parent, text="info", title= "INFO", size="", max_text_width=0):
        tk.Toplevel.__init__(self, parent)  # instead of super
        self.title(title)

        if max_text_width > 0:
            self.text = "\n".join(textwrap.wrap(text, width=int(max_text_width)))
        else:
            self.text = text


        if  not (size == ""):
            self.geometry(size)

        self.setup()


    def setup(self):
        ## MainFrame:
        self.MainFrame = tk.ttk.Frame(self, padding=(10,10))
        self.lbl_INFO =  ttk.Label(self.MainFrame, text=self.text)
        self.btn_OK = ttk.Button(self.MainFrame, text='Ok',
                             command=self.on_btn_OK)

        self.MainFrame.grid(column=0, row=0)
        self.lbl_INFO.grid( column=0, row=0)
        self.btn_OK.grid(   column=0, row=1)


        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        #self.MainFrame.columnconfigure(0, weight=1)
        #self.MainFrame.columnconfigure(1, weight=1)
        #self.MainFrame.columnconfigure(2, weight=1)

    def on_btn_OK(self):
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()  # first toplevel window
    root.title("Root")
    root.geometry("100x100")

    # random text: https://randomtextgenerator.com/
    text = """Way nor furnished sir procuring therefore but. Warmth far manner myself active are cannot called. Set her half end girl rich met. Me allowance departure an curiosity ye. In no talking address excited it conduct. Husbands debating replying overcame blessing he it me to domestic. 

Day handsome addition horrible sensible goodness two contempt. Evening for married his account removal. Estimable me disposing of be moonlight cordially curiosity. Delay rapid joy share allow age manor six. Went why far saw many knew. Exquisite excellent son gentleman acuteness her. Do is voice total power mr ye might round still. """

    print("\n".join(textwrap.wrap(text)))

    w1 = InfoWindow(root, text=text)
    w2 = InfoWindow(root, text=text, size="", max_text_width=30)
    w3 = InfoWindow(root, text=text, size="", max_text_width=80)
    root.mainloop()