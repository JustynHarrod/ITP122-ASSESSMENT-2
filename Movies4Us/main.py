import customtkinter as ctk
from PIL import Image
from backend import *
from logic_justyn import *
from logic_oren import *
from logic_james import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import random
import subprocess
import os
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MoviePosterWidget(ctk.CTkFrame):
    """Displays the selected movie poster."""
    def __init__(self, master):
        super().__init__(master, fg_color="#1a1d24", corner_radius=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        title_label = ctk.CTkLabel(
            self,
            text="Selected Movie",
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        )
        title_label.grid(row=0, column=0, pady=(20, 10))
        self.display_frame = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        self.display_frame.grid(
            row=1, column=0, sticky="nsew", padx=20, pady=(0, 20)
        )
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.poster_image = None
    def update_poster(self, index):
        """Updates the poster when a movie is selected."""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        movie = MOVIES_DATA[index]
        try:
            pil_img = Image.open(movie["poster"]).convert("RGB")
            self.poster_image = ctk.CTkImage(
                light_image=pil_img,
                dark_image=pil_img,
                size=(240, 340)
            )
            img_label = ctk.CTkLabel(
                self.display_frame,
                text="",
                image=self.poster_image
            )
            img_label.grid(row=0, column=0, pady=5)
        except (FileNotFoundError, OSError):
            img_label = ctk.CTkLabel(
                self.display_frame,
                text=f"No poster found\n{movie['title']}",
                text_color="#ffffff"
            )
            img_label.grid(row=0, column=0, pady=5)
        meta_label = ctk.CTkLabel(
            self.display_frame,
            text=f"{movie['title']} ({movie['rating']})",
            font=("Arial", 14, "bold"),
            text_color="#ffffff"
        )
        meta_label.grid(row=1, column=0, pady=(10, 0))

class MetricCard(ctk.CTkFrame):
    """Movie card displaying a poster, title and rating."""
    def __init__(self, master, movie, command=None):
        super().__init__(
            master,
            fg_color="#1a1d24",
            corner_radius=10,
            border_width=2,
            border_color="#2b2f38"
        )
        self.movie = movie
        self.command = command
        self.poster_image = None
        self.grid_columnconfigure(0, weight=1)
        try:
            pil_img = Image.open(movie["poster"]).convert("RGB")
            self.poster_image = ctk.CTkImage(
                light_image=pil_img,
                dark_image=pil_img,
                size=(150, 210)
            )
            poster_label = ctk.CTkLabel(self, text="", image=self.poster_image)
        except (FileNotFoundError, OSError, KeyError):
            poster_label = ctk.CTkLabel(
                self,
                text="No poster found",
                text_color="#8a93a0",
                height=210
            )
        poster_label.grid(row=0, column=0, padx=8, pady=(8, 4))
        title_label = ctk.CTkLabel(
            self,
            text=movie.get("title", "Unknown movie"),
            font=("Arial", 13, "bold"),
            text_color="#ffffff",
            wraplength=160
        )
        title_label.grid(row=1, column=0, padx=5, pady=4)
        rating_label = ctk.CTkLabel(
            self,
            text=f"Rating: {movie.get('rating', 'N/A')}",
            font=("Arial", 11),
            text_color="#8a93a0"
        )
        rating_label.grid(row=2, column=0, pady=(0, 10))
        # Makes the poster and its details clickable.
        for widget in (self, poster_label, title_label, rating_label):
            widget.bind("<Button-1>", self.select_movie)
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
    def select_movie(self, event=None):
        """Runs when the movie card is clicked."""
        if self.command:
            self.command()
    def on_enter(self, event=None):
        self.configure(border_color="#f59e0b")
    def on_leave(self, event=None):
        self.configure(border_color="#2b2f38")

class MovieInfoPopup(ctk.CTkToplevel):
    """Popup showing details for the selected movie."""
    def __init__(self, master, movie, on_checkout=None):
        super().__init__(master)
        self.movie = movie
        self.on_checkout = on_checkout
        self.poster_image = None
        self.title(movie.get("title", "Movie details"))
        self.geometry("1280x900")
        self.configure(fg_color="#0f1117")
        self.transient(master)
        self.grab_set()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        try:
            pil_img = Image.open(movie["poster"]).convert("RGB")
            self.poster_image = ctk.CTkImage(
                light_image=pil_img,
                dark_image=pil_img,
                size=(220, 320)
            )
            poster_label = ctk.CTkLabel(self, text="", image=self.poster_image)
        except (FileNotFoundError, OSError, KeyError):
            poster_label = ctk.CTkLabel(
                self,
                text="No poster found",
                text_color="#8a93a0",
                width=220,
                height=320
            )
        poster_label.grid(row=0, column=0, padx=25, pady=25, sticky="n")
        details = ctk.CTkFrame(self, fg_color="transparent")
        details.grid(row=0, column=1, padx=(0, 25), pady=25, sticky="nsew")
        details.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            details,
            text=movie.get("title", "Unknown movie"),
            font=("Arial", 22, "bold"),
            text_color="#ffffff",
            wraplength=530
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))
        ctk.CTkLabel(
            details,
            text=f"Rating: {movie.get('rating', 'N/A')}",
            font=("Arial", 14),
            text_color="#8a93a0"
        ).grid(row=1, column=0, sticky="w", pady=4)
        if movie.get("genre"):
            ctk.CTkLabel(
                details, text=f"Genre: {movie['genre']}",
                font=("Arial", 14), text_color="#8a93a0"
            ).grid(row=2, column=0, sticky="w", pady=4)
        if movie.get("runtime"):
            ctk.CTkLabel(
                details, text=f"Duration: {movie['runtime']} minutes",
                font=("Arial", 14), text_color="#8a93a0"
            ).grid(row=3, column=0, sticky="w", pady=4)
        session_list = movie.get("sessions", [])
        session_time = ", ".join(
        session["time"] for session in session_list if "time" in session
        ) if session_list else "No times available"
        ctk.CTkLabel(
            details,
            text=f"Sessions Available: {session_time}",
            font=("Arial", 14),
            text_color="#8a93a0"
            ).grid(row=4, column=0, sticky="w", pady=4)
        description = movie.get("description", "")
        if description:
            ctk.CTkLabel(
            details,
            text=description,
            font=("Arial", 13),
            text_color="#ffffff",
            wraplength=950,
            justify="left"
        ).grid(row=5, column=0, sticky="w", pady=(12, 15))
        buttons = ctk.CTkFrame(details, fg_color="transparent")
        buttons.grid(row=6, column=0, sticky="ew", pady=(20, 0))
        ctk.CTkButton(
            buttons,
            text="Continue to Checkout",
            fg_color="#f59e0b",
            hover_color="#8b5800",
            command=self.checkout
        ).pack(fill="x", pady=(0, 10))
        ctk.CTkButton(
            buttons,
            text="Back to Movies",
            fg_color="#2b2f38",
            hover_color="#3a3f4b",
            command=self.destroy
        ).pack(fill="x")

    def checkout(self):
        """Runs the checkout callback and closes the popup."""
        if self.on_checkout:
            self.on_checkout(self.movie)
        self.destroy()

class MainDashboard(ctk.CTk):
    """Main movie selection window."""
    def __init__(self):
        super().__init__()
        self.title("Movies4Us - Movie Selection - Melbourne Cinema")
        self.geometry("1280x900")
        self.configure(fg_color="#0f1117")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.selected_movie_index = 0
        self.movie_cards = []
        self.create_header()
        self.create_metrics_grid()
    def create_header(self):
        """Creates the heading at the top of the window."""
        header_frame = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        header_frame.grid(
            row=0, column=0, sticky="ew", padx=40, pady=(30, 20)
        )
        title = ctk.CTkLabel(
            header_frame,
            text="Movies4Us - Movie Selection Portal - Melbourne Cinema",
            font=("Arial", 26, "bold"),
            text_color="#ffffff"
        )
        title.pack()
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Choose a movie to get started today.",
            font=("Arial", 13),
            text_color="#8a93a0"
        )
        subtitle.pack(pady=(5, 0))
        staff_button = ctk.CTkButton(
        header_frame,
        text="Staff Login",
        font=("Arial", 13, "bold"),
        width=100,
        height=35,
        fg_color="#f59e0b",
        hover_color="#915d04",
        text_color="#ffffff",
        corner_radius=8,
        command=self.open_staff_portal
    )
        staff_button.place(relx=1.0, y=0, anchor="ne")
    def create_metrics_grid(self):
        """Creates the grid of clickable movie posters."""
        grid_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        grid_frame.grid(
            row=1, column=0, sticky="nsew", padx=40, pady=(0, 30)
        )
        for col in range(4):
            grid_frame.grid_columnconfigure(
                col, weight=1, uniform="col"
            )
        for index, movie in enumerate(MOVIES_DATA):
            row = index // 4
            col = index % 4
            card = MetricCard(
                grid_frame,
                movie=movie,
                command=lambda idx=index: self.select_movie(idx)
            )
            card.grid(
                row=row,
                column=col,
                sticky="n",
                padx=10,
                pady=10
            )
            self.movie_cards.append(card)
    def select_movie(self, index):
        """Opens the information popup for the selected movie."""
        if index < 0 or index >= len(MOVIES_DATA):
            return
        self.selected_movie_index = index
        movie = MOVIES_DATA[index]
        for i, card in enumerate(self.movie_cards):
            if i == index:
                card.configure(border_color="#f59e0b")
            else:
                card.configure(border_color="#2b2f38")
        MovieInfoPopup(self, movie, on_checkout=self.open_checkout)
    def open_checkout(self, movie):
        """Opens the customer checkout interface."""
        customer_ui_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "customer_ui.py"
        )
        try:
            subprocess.Popen([
                sys.executable,
                customer_ui_path
            ])
        except OSError as error:
            print(f"Could not open checkout: {error}")
    def on_close(self):
        """Closes the application."""
        plt.close("all")
        self.destroy()
    def open_staff_portal(self):
        """Opens the staff interface if staff_ui.py exists."""
        staff_ui_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "staff_ui.py"
        )
        try:
            subprocess.Popen([
                sys.executable,
                staff_ui_path
            ])
        except OSError as error:
            print(f"Could not open staff ui: {error}")

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()