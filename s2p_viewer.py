import tkinter as tk
import tkinter.font as tkFont
import skrf as rf
import os
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PlotButton:
    def __init__(self, root, text, command, color):
        self.button = tk.Button(root, bg=color, font=tkFont.Font(size=10),
                                fg="#000000", justify="center", text=text, command=command)

    def place(self, x, y, width, height):
        self.button.place(x=x, y=y, width=width, height=height)


class App:
    def __init__(self, root):
        root.title("S2P Viewer")
        root.configure(bg="#f0f0f0")
        root.iconbitmap("icon.ico")
        #root.iconphoto(False, tk.PhotoImage(file="icon.png"))
        width = 800
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.place(x=0, y=0, width=width, height=300)

        self.create_buttons(button_frame)

        graph_frame = tk.Frame(root, bg="#f0f0f0")
        graph_frame.place(x=10, y=45, width=width-100, height=height-55)

        self.fig = Figure(figsize=(6, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.plot_functions = {"S11": False, "S22": False,
                               "S12": False, "S21": False}

        self.ax.grid(True)
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Amplitude (dB)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        label_enzorg = tk.Label(root, text="EnzoRg", font=tkFont.Font(size=10))
        label_enzorg.pack(pady=20)
        label_enzorg.place(x=730, y=565, width=50, height=25)

    def create_buttons(self, root):
        button_open = PlotButton(root, "File", self.button_open_command, "#f0f0f0")
        button_open.place(x=10, y=10, width=50, height=25)

        button_help = PlotButton(root, "Save", self.button_save_command, "#f0f0f0")
        button_help.place(x=65, y=10, width=50, height=25)

        button_s11 = PlotButton(root, "S11", self.button_s11_command, "#f0f0f0")
        button_s11.place(x=730, y=45, width=50, height=25)

        button_s22 = PlotButton(root, "S22", self.button_s22_command, "#f0f0f0")
        button_s22.place(x=730, y=75, width=50, height=25)

        button_s12 = PlotButton(root, "S12", self.button_s12_command, "#f0f0f0")
        button_s12.place(x=730, y=105, width=50, height=25)

        button_s21 = PlotButton(root, "S21", self.button_s21_command, "#f0f0f0")
        button_s21.place(x=730, y=135, width=50, height=25)

        button_clean = PlotButton(root, "Clear", self.button_clear_command, "#79fc95")
        button_clean.place(x=730, y=185, width=50, height=25)

    file_path = ""

    def button_open_command(self):
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("S2P Files", "*.s2p")])

        if file_path:
            file_name = os.path.basename(file_path)
            self.fig.suptitle(file_name)
            self.fig.canvas.draw()

            for func in self.plot_functions:
                self.plot_functions[func] = False

        App.file_path = file_path

        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Amplitude (dB)")
        self.canvas.draw()

    def button_save_command(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

        if file_path:
            self.fig.savefig(file_path, format="png")

    def plot_s_db(self, m, n, label, color):
        global file_path
        if file_path:
            network = rf.Network(file_path)

            if not self.plot_functions[label]:
                network.plot_s_db(
                    m=m, n=n, label=label, color=color, ax=self.ax)
                self.ax.grid(True)
                self.ax.set_ylabel("Amplitude (dB)")
                self.canvas.draw()
                self.plot_functions[label] = True

    def button_s11_command(self):
        self.plot_s_db(0, 0, "S11", "#b7104d")

    def button_s22_command(self):
        self.plot_s_db(1, 1, "S22", "#10b77a")

    def button_s12_command(self):
        self.plot_s_db(0, 1, "S12", "#b79b10")

    def button_s21_command(self):
        self.plot_s_db(1, 0, "S21", "#1090b7")

    def button_clear_command(self):
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Amplitude (dB)")
        self.canvas.draw()

        for func in self.plot_functions:
            self.plot_functions[func] = False


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
