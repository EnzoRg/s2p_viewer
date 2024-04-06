__authors__ = "EnzoRg"
__GITPath___ = "https://github.com/EnzoRg/s2p_viewer"

import tkinter as tk
import tkinter.font as tkFont
import skrf as rf
import os
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PlotButton:
    def __init__(self, root, text, command, color, x, y, width, height):
        self.button = tk.Button(root, bg=color, font=tkFont.Font(size=10),
                                fg="#000000", justify="center", text=text, command=command)
        self.button.place(x=x, y=y, width=width, height=height)

class S2PViewerApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.plot_functions = {"S11": False, "S22": False, "S12": False, "S21": False}
        self.file_path = ""

    def setup_window(self):
        self.root.title("S2P Viewer")
        self.root.configure(bg="#f0f0f0")
        self.root.iconbitmap("icon.ico")
        width, height = 800, 600
        self.root.geometry(f"{width}x{height}+{int((self.root.winfo_screenwidth() - width) / 2)}+{int((self.root.winfo_screenheight() - height) / 2)}")
        self.root.resizable(width=False, height=False)

    def create_widgets(self):
        self.create_buttons()
        self.create_graph_frame()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.place(x=0, y=0, width=800, height=300)

        PlotButton(button_frame, "File", self.button_open_command, "#f0f0f0", 10, 10, 50, 25)
        PlotButton(button_frame, "Save", self.button_save_command, "#f0f0f0", 65, 10, 50, 25)
        PlotButton(button_frame, "S11", self.button_s_command(0, 0, "S11", "#b7104d"), "#f0f0f0", 730, 45, 50, 25)
        PlotButton(button_frame, "S22", self.button_s_command(1, 1, "S22", "#10b77a"), "#f0f0f0", 730, 75, 50, 25)
        PlotButton(button_frame, "S12", self.button_s_command(0, 1, "S12", "#b79b10"), "#f0f0f0", 730, 105, 50, 25)
        PlotButton(button_frame, "S21", self.button_s_command(1, 0, "S21", "#1090b7"), "#f0f0f0", 730, 135, 50, 25)
        PlotButton(button_frame, "Clear", self.button_clear_command, "#79fc95", 730, 185, 50, 25)

    def create_graph_frame(self):
        graph_frame = tk.Frame(self.root, bg="#f0f0f0")
        graph_frame.place(x=10, y=45, width=690, height=545)

        self.fig = Figure(figsize=(6, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Amplitude (dB)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def button_open_command(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("S2P Files", "*.s2p")])
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            self.fig.suptitle(file_name)
            self.fig.canvas.draw()
            self.plot_functions = {func: False for func in self.plot_functions}
        self.clear_plot()

    def button_save_command(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.fig.savefig(file_path, format="png")

    def button_s_command(self, m, n, label, color):
        def command():
            if self.file_path:
                network = rf.Network(self.file_path)
                if not self.plot_functions[label]:
                    network.plot_s_db(m=m, n=n, label=label, color=color, ax=self.ax)
                    self.ax.grid(True)
                    self.ax.set_ylabel("Amplitude (dB)")
                    self.canvas.draw()
                    self.plot_functions[label] = True
        return command

    def clear_plot(self):
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Amplitude (dB)")
        self.canvas.draw()
        self.plot_functions = {func: False for func in self.plot_functions}

    def button_clear_command(self):
        self.clear_plot()

if __name__ == "__main__":
    root = tk.Tk()
    app = S2PViewerApp(root)
    root.mainloop()
