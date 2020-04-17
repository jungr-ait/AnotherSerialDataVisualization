import tkinter as tk
from tkinter import ttk


class YScrollListbox_Widget(tk.Frame):
    def __init__(self, parent, buffer_size  = 0, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        ### widgets
        self.lst = tk.Listbox(self)
        self.scrl = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.lst.yview)
        self.lst['yscrollcommand'] = self.scrl.set
        self.lst.insert('end', 'empty...')

        self.pack(fill="both", expand=True)
        self.lst.pack(side="left", fill="both", expand=True)
        self.scrl.pack(side="left", fill="y")
        self.buffer_size = buffer_size

    def clear_listbox(self):
        self.lst.delete(0, self.lst.size())

    def size_listbox(self):
        return self.lst.size()

    def append_line(self, line):
        self.lst.insert('end', line)
        if self.buffer_size > 0:
            if self.lst.size() > self.buffer_size:
                self.lst.delete(0, self.lst.size() - self.buffer_size)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('YScrollListbox_Widget - Test')
    root.geometry("480x300")
    w = YScrollListbox_Widget(root, buffer_size=10)


    for i in range(1,100):
        w.append_line(str(i))
    root.mainloop()