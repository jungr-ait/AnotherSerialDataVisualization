import tkinter as tk

class Example():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("some application")

        # menu left
        self.menu_left = tk.Frame(self.root, width=150, bg="#ababab")
        self.menu_left_upper = tk.Frame(self.menu_left, bg="red")
        self.menu_left_lower = tk.Frame(self.menu_left, bg="blue")

        self.test = tk.Label(self.menu_left_upper, text="test")
        self.test.pack()
        self.menu_left_upper.pack(side="top", fill="both", expand=True)

        self.test_lo = tk.Label(self.menu_left_lower, text="test")
        self.test_lo.pack()
        self.menu_left_lower.pack(side="top", fill="both", expand=True)

        # right area
        self.some_title_frame = tk.Frame(self.root, bg="#dfdfdf")

        self.some_title = tk.Label(self.some_title_frame, text="some title", bg="#dfdfdf")
        self.some_title.pack()

        self.canvas_area = tk.Canvas(self.root, width=500, height=400, background="#ffffff")
        self.canvas_area.grid(row=1, column=1)

        # status bar
        self.status_frame = tk.Frame(self.root)
        self.status = tk.Label(self.status_frame, text="this is the status bar")
        self.status.pack(fill="both", expand=True)

        self.menu_left.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.menu_left.columnconfigure(0, weight=1)
        self.some_title_frame.grid(row=0, column=1, sticky="ew")
        self.canvas_area.grid(row=1, column=1, sticky="nsew")
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.root.mainloop()

if __name__ == '__main__':
    Example()