import customtkinter as ctk
from PIL import Image
import backend, logic_justyn
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MetricCard(ctk.CTkFrame):
    """Reusable card with content perfectly centered both horizontally and vertically."""
    def __init__(self, master, title, value, subtitle=""):
        super().__init__(master, fg_color="#1a1d24", corner_radius=10)
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        self.title_label = ctk.CTkLabel(container, text=title, font=("Arial", 12), text_color="#8a93a0", anchor="center", justify="center")
        self.title_label.pack(anchor="center", pady=(0, 4))
        val_str = str(value)
        font_size = 13 if "\n" in val_str or len(val_str) > 18 else 24
        self.value_label = ctk.CTkLabel(container, text=val_str, font=("Arial", font_size, "bold"), text_color="#ffffff", anchor="center", justify="center")
        self.value_label.pack(anchor="center", pady=(0, 4))
        if subtitle:
            self.sub_label = ctk.CTkLabel(container, text=subtitle, font=("Arial", 11), text_color="#6c757d", anchor="center", justify="center")
            self.sub_label.pack(anchor="center")
        else:
            self.configure(height=100)

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
        for index, movie in enumerate(backend.MOVIES_DATA):
            btn = ctk.CTkButton(self.nav_frame, text=movie["title"], font=("Arial", 12), fg_color="#2b2f38", hover_color="#3a3f4b", text_color="#ffffff", height=30, command=lambda idx=index: self.switch_movie(idx))
            btn.pack(side="left", padx=4)

    def switch_movie(self, index):
        """Switches active movie data, updates UI components, and triggers external callback."""
        self.current_movie_index = index
        self.load_movie_data(index)
        if self.on_movie_change:
            self.on_movie_change(index)

    def load_movie_data(self, index):
        """Clears and re-builds session bars, occupancy stats, and the movie-specific pie chart."""
        for widget in self.left_sub.winfo_children():
            widget.destroy()
        movie = backend.MOVIES_DATA[index]
        total_capacity = sum(s["capacity"] for s in movie["sessions"])
        total_remaining = sum(s["tickets_remaining"] for s in movie["sessions"])
        total_sold = total_capacity - total_remaining
        occupancy_rate = (total_sold / total_capacity * 100) if total_capacity > 0 else 0
        self.left_sub.grid_columnconfigure(0, weight=1)
        self.left_sub.grid_rowconfigure(0, weight=0)
        self.left_sub.grid_rowconfigure(1, weight=1)
        self.left_sub.grid_rowconfigure(2, weight=0)
        info_frame = ctk.CTkFrame(self.left_sub, fg_color="#2b2f38", corner_radius=6)
        info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        info_frame.grid_columnconfigure(0, weight=1)
        meta_text = f"Genre: {movie['genre']}  |  Runtime: {movie['runtime']} mins"
        meta_label = ctk.CTkLabel(info_frame, text=meta_text, font=("Arial", 11), text_color="#8a93a0", justify="center")
        meta_label.pack(pady=8, padx=10)
        sessions_frame = ctk.CTkFrame(self.left_sub, fg_color="transparent")
        sessions_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        sessions_frame.grid_columnconfigure(0, weight=1)

        for r_idx, session in enumerate(movie["sessions"]):
            capacity = session["capacity"]
            remaining = session["tickets_remaining"]
            sold = capacity - remaining
            progress_val = sold / capacity if capacity > 0 else 0
            row_frame = ctk.CTkFrame(sessions_frame, fg_color="transparent")
            row_frame.grid(row=r_idx, column=0, sticky="ew", pady=4)
            row_frame.grid_columnconfigure(1, weight=1)
            time_label = ctk.CTkLabel(row_frame, text=session["time"], font=("Arial", 11, "bold"), text_color="#ffffff", width=70, anchor="w")
            time_label.grid(row=0, column=0, sticky="w")
            p_bar = ctk.CTkProgressBar(row_frame, progress_color="#f59e0b", fg_color="#1a1d24", height=8)
            p_bar.set(progress_val)
            p_bar.grid(row=0, column=1, sticky="ew", padx=10)
            count_label = ctk.CTkLabel(row_frame, text=f"{sold}/{capacity}", font=("Arial", 11), text_color="#8a93a0", width=45, anchor="e")
            count_label.grid(row=0, column=2, sticky="e")
        occupancy_card = ctk.CTkFrame(self.left_sub, fg_color="#14171f", corner_radius=8)
        occupancy_card.grid(row=2, column=0, sticky="nsew", pady=(5, 0))
        occupancy_card.grid_columnconfigure(0, weight=1)
        occupancy_card.grid_rowconfigure(0, weight=1)
        occ_text = f"Overall Occupancy Rate: {occupancy_rate:.1f}%"
        occ_label = ctk.CTkLabel(occupancy_card, text=occ_text, font=("Arial", 14, "bold"), text_color="#f59e0b")
        occ_label.grid(row=0, column=0, padx=15, pady=12)
        adults = int(total_sold * 0.6)
        children = int(total_sold * 0.2)
        concessions = total_sold - adults - children  
        labels = ['Adult', 'Child', 'Conc.']
        sizes = [max(0, adults), max(0, children), max(0, concessions)]
        colors = ['#f59e0b', '#3b82f6', '#10b981']
        if self.fig is None:
            self.fig, self.ax = plt.subplots(figsize=(3, 3), facecolor="#14171f")
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_sub)
            self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=5, pady=5)
        else:
            self.ax.clear()
        self.ax.set_facecolor("#14171f")
        if total_sold > 0:
            self.ax.pie(sizes, labels=labels, colors=colors, textprops={'color': 'white', 'fontsize': 9}, autopct='%1.0f%%', pctdistance=0.75, startangle=90)
        else:
            self.ax.text(0, 0, "No Sales Yet", color="#8a93a0", fontsize=10, ha='center', va='center')
        self.ax.set_title("Ticket Types", color="white", fontsize=11, pad=5)
        self.fig.tight_layout(pad=1)
        self.canvas.draw()

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
        self.update_poster(0)

    def update_poster(self, index):
        """Loads and scales the poster image to fill ~90% of the display area."""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        movie = backend.MOVIES_DATA[index]
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

class StaffDashboardWindow(ctk.CTk):
    """Standalone Staff Dashboard Window using grid layout"""
    def __init__(self):
        super().__init__()
        self.title("Movies4Us - Staff Portal")
        self.geometry("1280x900")
        self.configure(fg_color="#0f1117")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        logic_justyn.initialize_random_sales()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=0) # Metrics
        self.grid_rowconfigure(2, weight=1) # Row 2 Content
        self.report_data = logic_justyn.generate_sales_report()
        self.create_header()
        self.create_metrics_grid()
        self.create_row_two()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(30, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        title = ctk.CTkLabel(header_frame, text="Staff Portal", font=("Arial", 26, "bold"), text_color="#ffffff")
        title.grid(row=0, column=0, sticky="n")
        subtitle = ctk.CTkLabel(header_frame, text=("Access ticket sales, availability reports, and cinema performance."), font=("Arial", 13), text_color="#8a93a0")
        subtitle.grid(row=1, column=0, sticky="n", pady=(5, 0))

    def create_metrics_grid(self):
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.grid(row=1, column=0, sticky="new", padx=40, pady=10)
        grid_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
        card_sold = MetricCard(grid_frame, title="Tickets Sold", value=self.report_data["total_sales"], subtitle=f"Across {sum(len(m['sessions']) for m in backend.MOVIES_DATA)} screenings of {len(backend.MOVIES_DATA)} movies")
        card_sold.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        formatted_revenue = f"${self.report_data['revenue']:,.0f}"
        card_rev = MetricCard(grid_frame, title="Ticket Revenue", value=formatted_revenue, subtitle=f"Avg: ${self.report_data['average_ticket_price']:.2f}")
        card_rev.grid(row=0, column=1, sticky="nsew", padx=10)
        top_str = ", ".join(self.report_data["top_movies"]) if self.report_data["top_movies"] else "N/A"
        card_top = MetricCard(grid_frame, title="Top Selling", value=top_str, subtitle="")
        card_top.grid(row=0, column=2, sticky="nsew", padx=10)
        low_str = "\n".join(self.report_data["lowest_movies"]) if self.report_data["lowest_movies"] else "N/A"
        card_low = MetricCard(grid_frame, title="Lowest Performing", value=low_str, subtitle="")
        card_low.grid(row=0, column=3, sticky="nsew", padx=(10, 0))

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

    def on_close(self):
        """Cleanly closes Matplotlib figures and exits application without trailing after-script errors."""
        plt.close('all')
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = StaffDashboardWindow()
    app.mainloop()