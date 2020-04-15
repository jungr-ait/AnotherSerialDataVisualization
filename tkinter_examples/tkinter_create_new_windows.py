import tkinter as tk
import tkinter.ttk as ttk


class NiceWindow(tk.Toplevel):
    def __init__(self, parent, title= "I am a NiceWindow!"):
        tk.Toplevel.__init__(self, parent)  # instead of super
        self.title(title)

        self.geometry('300x200+100+100')


class MainGUI(tk.Tk):  # a tk.Toplevel
    window_handles = {}  # dictionary holding our nice windows...

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('MainGUI')
        self.root = self   # here is your root, when you are looking for it!

        self.btn_create = ttk.Button(self, text='create window', command=self.on_btn_create)
        self.btn_create.pack()
        self.btn_clear = ttk.Button(self, text='kill windows', command=self.on_btn_kill)
        self.btn_clear.pack()
        self.btn_quit = ttk.Button(self, text='quit', command=self.on_btn_quit)
        self.btn_quit.pack()


    def on_btn_create(self):
        print('button create pressed')
        self.window_handles[len(self.window_handles)] = NiceWindow(self.root)

    def on_btn_kill(self):
        print('on_btn_kill pressed')
        for key in self.window_handles:
            self.window_handles[key].destroy()

        self.window_handles = {}

    def on_btn_quit(self):
        print('quit')
        self.quit()


if __name__ == '__main__':
    app = MainGUI()
    app.geometry('300x600')
    app.mainloop()