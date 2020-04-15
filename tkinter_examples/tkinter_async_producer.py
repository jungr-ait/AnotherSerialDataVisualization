# classical producer consumer example
import tkinter as tk
import tkinter.ttk as ttk






class ConsumerGUI(tk.Tk):  # a tk.Toplevel
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("MainGUI")
        self.root = self   # here is your root, when you are looking for it!


        self.content = ttk.Frame(self, padding=10 )
        self.btn1 = ttk.Button(self, text='create consumer', command=self.on_btn1)
        self.btn1.pack()
        self.btn2 = ttk.Button(self, text='stop', command=self.on_btn2)
        self.btn2.pack()
        self.btn_quit = ttk.Button(self, text='quit', command=self.on_btn_quit)
        self.btn_quit.pack()
        # data field
        self.frame_DataView = ttk.Frame(self, padding=10, height=100 )
        self.lst_DataView = tk.Listbox(self.frame_DataView)
        self.scrl_DataView = ttk.Scrollbar(self.frame_DataView, orient=tk.VERTICAL, command=self.lst_DataView.yview)
        self.lst_DataView['yscrollcommand'] = self.scrl_DataView.set
        self.lst_DataView.insert('end', 'empty...')
        self.lst_DataView.size()
        self.lst_DataView_buffersize  = 50 # max buffersize in listbox.
        self.scrl_DataView.pack(side=tk.RIGHT, fill=tk.Y)
        self.lst_DataView.pack()
        self.frame_DataView.pack()


    def __del__(self):
        print("kill object....")

    def on_btn1(self):
        print("btn1 pressed")

    def on_btn2(self):
        print("btn2 pressed")

    def on_btn_quit(self):
        print("quit")
        self.quit()

if __name__ == '__main__':
    app = ConsumerGUI()
    app.geometry("300x600")
    app.mainloop()



