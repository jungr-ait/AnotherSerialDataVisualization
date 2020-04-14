from tkinter import *
from tkinter import ttk



def create_frame(root, name):
    content = ttk.Frame(root, padding=(3, 3, 12, 12))
    frame = ttk.Frame(content, borderwidth=5, relief="sunken", width=200, height=100)
    namelbl = ttk.Label(content, text="Name")
    name = ttk.Entry(content)
    name.focus()
    ok1 = ttk.Button(content, text="ok", command=lambda: print("ok pressed"))

    onevar = BooleanVar()
    twovar = BooleanVar()
    threevar = BooleanVar()

    onevar.set(True)
    twovar.set(False)
    threevar.set(True)

    one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
    two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
    three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
    ok = ttk.Button(content, text="Okay", command=lambda: print("ok pressed"))
    cancel = ttk.Button(content, text="Cancel", command=lambda: print("cancel pressed"))
    quit = ttk.Button(content, text="Quit", command=root.destroy)

    content.grid(column=0, row=0, sticky=(N, S, E, W))
    frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
    namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), pady=0, padx=5)
    name.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
    ok1.grid(column=3, row=2, columnspan=2, sticky=(N, E, W))
    one.grid(column=0, row=3)
    two.grid(column=1, row=3)
    three.grid(column=2, row=3)
    ok.grid(column=3, row=3)
    cancel.grid(column=4, row=3)
    quit.grid(column=6, row=3)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    content.columnconfigure(0, weight=3)
    content.columnconfigure(1, weight=3)
    content.columnconfigure(2, weight=3)
    content.columnconfigure(3, weight=1)
    content.columnconfigure(4, weight=1)
    content.rowconfigure(1, weight=1)
    return content


root = Tk() # first toplevel window
root.title("toplevel1")
frame1 = create_frame(root, name="frame1")

root2 = Tk() # second toplevel window
## or:
#root2 =  Toplevel(root) # Attention: when root is destroyed, root2 will also be destroyed!
root2.title("toplevel2")
frame2 = create_frame(root2, name="frame2")



root.mainloop()