import tkinter as tk


class MainWindow(tk.Frame):
    """
    Class definition of main window with canvas to be drawn on
    """
    def __init__(self, title, master=None, width=800, height=500):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title(title)
        # Set geometry of window
        h_shift = (self.master.winfo_screenwidth() - width) // 2    # horizontal shift: align central
        v_shift = (self.master.winfo_screenheight() - height) // 2  # vertical shift: align central
        self.master.geometry(f'{width:d}x{height:d}+{h_shift:d}+{v_shift:d}')

        self.canvas = tk.Canvas(self, width=width, height=height, bg='white')
        self.canvas.grid(row=0, column=0)

        self.canvas.bind('<Button-1>', self.click)

    def click(self, event):
        pos = (event.x, event.y)
        print(pos)

if __name__ == '__main__':
    app = MainWindow(title='Testing the MainWindow-Class')
    app.mainloop()
