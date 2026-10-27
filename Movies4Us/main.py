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

class MovieAvailabilityWidget(ctk.CTkFrame):
    """Interactive panel with movie selector tabs, session progress bars, pie chart, and occupancy rate."""
    def __init__(self, master, on_movie_change=None):
        super().__init__(master, fg_color="#1a1d24", corner_radius=10)
        self.on_movie_change = on_movie_change
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)   
        title_label = ctk.CTkLabel(self, text="Movie Performance & Breakdown", font=("Arial", 16, "bold"), text_color="#ffffff")
        title_label.grid(row=0, column=0, sticky="n", padx=15, pady=(15, 10))
        self.nav_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", fg_color="transparent", height=45)
        self.nav_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(1, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.left_sub = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.left_sub.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.right_sub = ctk.CTkFrame(self.content_container, fg_color="#14171f", corner_radius=8)
        self.right_sub.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.right_sub.grid_columnconfigure(0, weight=1)
        self.right_sub.grid_rowconfigure(0, weight=1)
        self.fig = None
        self.ax = None
        self.canvas = None
        self.current_movie_index = 0
        self.create_movie_tabs()
        self.load_movie_data(self.current_movie_index)

    def create_movie_tabs(self):
        """Creates clickable buttons at the top for each movie."""
        for index, movie in enumerate(MOVIES_DATA):
            btn = ctk.CTkButton(self.nav_frame, text=movie["title"], font=("Arial", 12), fg_color="#2b2f38", hover_color="#3a3f4b", text_color="#ffffff", height=30, command=lambda idx=index: self.switch_movie(idx))
            btn.pack(side="left", padx=4)

class MoviePosterWidget(ctk.CTkFrame):
    """Panel displaying the selected movie poster filling ~90% of container space."""
    def __init__(self, master):
        super().__init__(master, fg_color="#1a1d24", corner_radius=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        title_label = ctk.CTkLabel(self, text="Selected Movie Spotlight", font=("Arial", 16, "bold"), text_color="#ffffff")
        title_label.grid(row=0, column=0, sticky="n", padx=20, pady=(20, 10))
        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)

    def update_poster(self, index):
        """Loads and scales the poster image to fill ~90% of the display area."""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        movie = MOVIES_DATA[index]
        try:
            pil_img = Image.open(movie["poster"])
            movie_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(240, 340))
            img_label = ctk.CTkLabel(self.display_frame, text="", image=movie_image)
            img_label.grid(row=0, column=0, sticky="nsew", pady=5)
        except Exception:
            fallback_box = ctk.CTkFrame(self.display_frame, fg_color="#2b2f38", corner_radius=6)
            fallback_box.grid(row=0, column=0, sticky="nsew", pady=5)
            fallback_label = ctk.CTkLabel(fallback_box, text=f"No poster found\n({movie['title']})", font=("Arial", 12), text_color="#ffffff")
            fallback_label.place(relx=0.5, rely=0.5, anchor="center")
        meta_label = ctk.CTkLabel(self.display_frame, text=f"{movie['title']} ({movie['rating']})", font=("Arial", 14, "bold"), text_color="#ffffff")
        meta_label.grid(row=1, column=0, pady=(10, 0))

class MetricCard(ctk.CTkFrame):
    """Reusable card with content perfectly centered both horizontally and vertically."""
    def __init__(self, master, title, subtitle="", poster=None):
        super().__init__(master, fg_color="#1a1d24", corner_radius=10)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        self.title_label = ctk.CTkLabel(container, text=title, font=("Arial", 12), text_color="#8a93a0", anchor="center", justify="center")
        self.title_label.pack(anchor="center", pady=(0, 4))
        if subtitle:
            self.sub_label = ctk.CTkLabel(container, text=subtitle, font=("Arial", 11), text_color="#6c757d", anchor="center", justify="center")
            self.sub_label.pack(anchor="center")
        else:
            self.configure(height=100)

class MainDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Movies4Us - Movie Selection - Melbourne Cinema")
        self.geometry("1280x900")
        self.configure(fg_color="#0f1117")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=0) # Metrics
        self.grid_rowconfigure(2, weight=1) # Row 2 Content
        self.create_header()
        self.create_metrics_grid()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(30, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        title = ctk.CTkLabel(header_frame, text="Movie Selection Portal", font=("Arial", 26, "bold"), text_color="#ffffff")
        title.grid(row=0, column=0, sticky="n")
        subtitle = ctk.CTkLabel(header_frame, text=("Play the movie. Ya ya"), font=("Arial", 13), text_color="#8a93a0")
        subtitle.grid(row=1, column=0, sticky="n", pady=(5, 0))

    def on_close(self):
        """Cleanly closes Matplotlib figures and exits application without trailing after-script errors."""
        plt.close('all')
        self.destroy()
        sys.exit(0)

    def create_metrics_grid(self):
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.grid_rowconfigure((0), weight=1, uniform="row")
        grid_frame.grid(row=0, column=0, sticky="new", padx=40, pady=30)
        grid_frame.grid_rowconfigure((1), weight=1, uniform="row")
        grid_frame.grid(row=1, column=0, sticky="new", padx=40, pady=30)
        grid_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
        card_movie1 = MetricCard(grid_frame, title="Street Fighter", subtitle="M | Action | 119 minutes", poster="images/streetfighter.png")
        card_movie1.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        card_movie2 = MetricCard(grid_frame, title="Movie 2", subtitle="1234")
        card_movie2.grid(row=0, column=1, sticky="ew", padx=10)
        card_movie3 = MetricCard(grid_frame, title="Movie 3", subtitle="1234")
        card_movie3.grid(row=0, column=2, sticky="ew", padx=10)
        card_movie4 = MetricCard(grid_frame, title="Movie 4", subtitle="1234")
        card_movie4.grid(row=0, column=3, sticky="ew", padx=(10, 0))
        card_movie5 = MetricCard(grid_frame, title="Movie 5", subtitle="1234")
        card_movie5.grid(row=2, column=0, sticky="ew", padx=(0, 10))
        card_movie6 = MetricCard(grid_frame, title="Movie 6", subtitle="1234")
        card_movie6.grid(row=2, column=1, sticky="ew", padx=10)
        card_movie7 = MetricCard(grid_frame, title="Movie 7", subtitle="1234")
        card_movie7.grid(row=2, column=2, sticky="ew", padx=10)
        card_movie8 = MetricCard(grid_frame, title="Movie 8", subtitle="1234")
        card_movie8.grid(row=2, column=3, sticky="ew", padx=(10, 0))


    def create_row_two(self):
        """Splits Row 2 into 2 columns for the session slider and large poster spotlight."""
        row2_frame = ctk.CTkFrame(self, fg_color="transparent")
        row2_frame.grid(row=2, column=0, sticky="nsew", padx=40, pady=(10, 30))
        row2_frame.grid_columnconfigure(0, weight=2)
        row2_frame.grid_columnconfigure(1, weight=1)
        row2_frame.grid_rowconfigure(0, weight=1)
        self.poster_widget = MoviePosterWidget(row2_frame)
        self.poster_widget.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        movie_panel = MovieAvailabilityWidget(row2_frame, on_movie_change=self.poster_widget.update_poster)
        movie_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()

