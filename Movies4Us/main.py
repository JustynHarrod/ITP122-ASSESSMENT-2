import customtkinter as ctk
from PIL import Image
from backend import *
from logic_justyn import *
from logic_oren import *
from logic_james import *
from logic_wayne import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MainDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Movies4Us - Movie Selection - Melbourne Cinema")
        self.geometry("1280x900")
        self.configure(fg_color="#0f1117")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Cleanly closes Matplotlib figures and exits application without trailing after-script errors."""
        plt.close('all')
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()

