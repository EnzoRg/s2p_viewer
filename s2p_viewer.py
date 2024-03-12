import tkinter as tk
import tkinter.font as tkFont
import skrf as rf
import os
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class App:
    def __init__(self, root):
        root.title("S2P Viewer - EnzoRg")
        width = 770
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.plot_functions = {'S11': False, 'S22': False, 'S12': False, 'S21': False,}

        self.ax.grid(True)
        self.ax.set_xlabel('Frequency [Hz]')
        self.ax.set_ylabel('Amplitude [dB]')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        button_open = tk.Button(root, bg="#f0f0f0", font=tkFont.Font(size=10), fg="#000000", justify="center", text="Open", command=self.button_open_command)
        button_open.place(x=10, y=10, width=70, height=25)

        button_s11 = tk.Button(root, bg="#f0f0f0", font=tkFont.Font(size=10), fg="#000000", justify="center", text="S11", command=self.button_s11_command)
        button_s11.place(x=90, y=10, width=70, height=25)

        button_s22 = tk.Button(root, bg="#f0f0f0", font=tkFont.Font(size=10), fg="#000000", justify="center", text="S22", command=self.button_s22_command)
        button_s22.place(x=170, y=10, width=70, height=25)

        button_s12 = tk.Button(root, bg="#f0f0f0", font=tkFont.Font(size=10), fg="#000000", justify="center", text="S12", command=self.button_s12_command)
        button_s12.place(x=250, y=10, width=70, height=25)

        button_s21 = tk.Button(root, bg="#f0f0f0", font=tkFont.Font(size=10), fg="#000000", justify="center", text="S21", command=self.button_s21_command)
        button_s21.place(x=330, y=10, width=70, height=25)

        button_clean = tk.Button(root, bg="#f0f0f0", font=tkFont.Font(size=10), fg="#000000", justify="center", text="Clear", command=self.button_clean_command)
        button_clean.place(x=410, y=10, width=70, height=25)

        self.file_path_label = tk.Label(root, text="", font=tkFont.Font(size=10), justify="left", wraplength=width-20)
        self.file_path_label.place(x=500, y=12)

    def button_open_command(self):
        print("command: Open")
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[('S2P Files', '*.s2p')])
        print(file_path)

        file_name = os.path.basename(file_path)

        # Actualizar el Label con el nuevo file_path
        self.file_path_label.config(text=f"File: {file_name}")

    def plot_s_db(self, m, n, label):
        global file_path
        if file_path:
            network = rf.Network(file_path)
            
            if not self.plot_functions[label]:  
                network.plot_s_db(m=m, n=n, label=label, ax=self.ax)
                self.ax.grid(True)
                self.ax.set_xlabel('Frequency [Hz]')
                self.ax.set_ylabel('Amplitude [dB]')
                self.canvas.draw()

                self.plot_functions[label] = True

    def button_s11_command(self):
        print("command: S11")
        self.plot_s_db(0, 0, 'S11')

    def button_s22_command(self):
        print("command: S22")
        self.plot_s_db(1, 1, 'S22')

    def button_s12_command(self):
        print("command: S12")
        self.plot_s_db(0, 1, 'S12')

    def button_s21_command(self):
        print("command: S21")
        self.plot_s_db(1, 0, 'S21')

    def button_clean_command(self):
        print("command: Clean")
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_xlabel('Frequency [Hz]')
        self.ax.set_ylabel('Amplitude [dB]')
        self.canvas.draw()

        for func in self.plot_functions:
            self.plot_functions[func] = False

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = App(root)
    root.mainloop()
