import tkinter as tk
import tkinter.filedialog as filedialog
from network import Network

colors = ['blue', 'black', 'red', 'green', 'white', 'cyan', 'yellow', 'magenta']
fonts = ['Purisa', 'Helvetica', 'Times']


class MainWindow(tk.Frame):
    """
    Class definition of main window with canvas to be drawn on
    """

    def __init__(self, title, master=None, width=800, height=500):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title(title)
        # Set geometry of window
        h_shift = (self.master.winfo_screenwidth() - width) // 2  # horizontal shift: align central
        v_shift = (self.master.winfo_screenheight() - height) // 2  # vertical shift: align central
        self.master.geometry(f'{width:d}x{height:d}+{h_shift:d}+{v_shift:d}')

        self.canvas = tk.Canvas(self, width=width, height=height, bg='white')
        self.canvas.grid(row=0, column=0)

        self.network = Network()
        self.highlighted = None

        self.canvas.bind('<Button-1>', self.click)
        self.bind_all('<Control-s>', self.save)
        self.bind_all('<Control-l>', self.load)

    def click(self, event):
        pos = (event.x, event.y)
        # Check if clicked on existing element
        click_id = event.widget.find_withtag('current')
        if click_id:
            shape_ids = [el.shape for el in self.network.elements]
            text_ids = [el.text for el in self.network.elements]
            if click_id[0] in shape_ids:
                el = self.network.elements[shape_ids.index(click_id[0])]
                self.highlight(el)
                return
            elif click_id[0] in text_ids:
                el = self.network.elements[text_ids.index(click_id[0])]
                self.highlight(el)
                return
        # If not add elements: Master first
        else:
            data = {}
            new_window = tk.Toplevel(self.master)
            if self.network.master is None:
                SetupWindow(new_window, data, default_color='blue')
            else:
                SetupWindow(new_window, data, default_color='green')
            self.master.wait_window(new_window)
            if self.network.master is None:
                self.network.add_master(pos, **data)
            else:
                if self.highlighted:
                    parent = self.highlighted
                else:
                    parent = self.network.master
                self.network.add_element(parent, pos, **data)
        self.network.draw(self.canvas)

    def highlight(self, element):
        if self.highlighted is not None:
            self.highlighted.switch_highlight(self.canvas)
        self.highlighted = element
        self.highlighted.switch_highlight(self.canvas)

    def save(self, event):
        if self.network.master is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension='json')
        if not file_path:
            return
        self.network.save(file_path)
        print('Saved Network to ' + file_path)

    def load(self, event):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.network = Network.from_json(file_path)
        self.network.draw(self.canvas)
        print('Loaded Network from ' + file_path)


class SetupWindow(tk.Frame):
    def __init__(self, master, data, default_color='blue'):
        tk.Frame.__init__(self, master)
        self.grid()
        self.data = data
        self.master.title('')
        self.master.resizable(width=False, height=False)
        # # Set geometry of window
        # h_shift = (self.master.winfo_screenwidth() - width) // 2  # horizontal shift: align central
        # v_shift = (self.master.winfo_screenheight() - height) // 2  # vertical shift: align central
        # self.master.geometry(f'{width:d}x{height:d}+{h_shift:d}+{v_shift:d}')
        # Textbox for string
        self.text_box = tk.Text(self, height=2, width=15)
        self.text_box.grid(row=0, column=0)
        self.text_box.focus_set()
        # Dropdown list for color
        tk.Label(self, text='Fill Color').grid(row=1, column=0, sticky=tk.W)
        self.color_var = tk.StringVar()
        self.color_var.set(default_color)
        self.color_menu = tk.OptionMenu(self, self.color_var, *colors)
        self.color_menu.grid(row=2, column=0)
        # Dropdown list for font
        tk.Label(self, text='Font').grid(row=3, column=0, sticky=tk.W)
        self.font_var = tk.StringVar()
        self.font_var.set(fonts[0])
        self.font_menu = tk.OptionMenu(self, self.font_var, *fonts)
        self.font_menu.grid(row=4, column=0)
        # OK button
        tk.Button(self, text='OK', command=self.return_values).grid(row=5, column=0, sticky='EW')
        self.bind_all('<Return>', self.return_values)

    def return_values(self, *args):
        self.data['s'] = self.text_box.get('1.0', tk.END).rstrip()
        self.data['fill_color'] = self.color_var.get()
        self.data['font'] = (self.font_var.get(), 12)
        self.master.destroy()


if __name__ == '__main__':
    app = MainWindow(title='Testing the MainWindow-Class')
    app.mainloop()
