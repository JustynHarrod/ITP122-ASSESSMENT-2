import tkinter as tk
from tkinter import ttk, messagebox
import os

movies = [
    {
        "title": "Avatar: The Way of Water",
        "genre": "Sci-Fi / Action",
        "rating": "PG-13",
        "image": "avatar.png"
    },
    {
        "title": "Inside Out 2",
        "genre": "Animation / Family",
        "rating": "PG",
        "image": "insideout2.png"
    },
    {
        "title": "Dune: Part Two",
        "genre": "Sci-Fi / Adventure",
        "rating": "PG-13",
        "image": "dunepart2.png"
    },
    {
        "title": "Oppenheimer",
        "genre": "Biography / Drama",
        "rating": "MA15+",
        "image": "oppenheimer.png"
    },
]

def open_staff_login():
    """Handles staff login link click."""
    messagebox.showinfo("Satff Login", "Staff Login modal will open here. \n\nThis will grant access to logical module 2: Operational reports.")

def show_movie_info(movie_title):
    """Displays movie details."""
    messagebox.showinfo("Movie Info", f"Detailed synopsis, director, and cast info for: \n\n🎥 {movie_title}")

def show_session_times(movie_title):
    """Displays available screening sessions."""
    sessions = "• Today: 1:30 PM, 4:45 PM, 7:15 PM, 9:30 PM"
    messagebox.showinfo("Session Times", f"Screening Schedule for {movie_title}:\n\n{sessions}")

def buy_tickets(movie_title):
    """Triggers the ticket purchase flow (Logical Module 1)."""
    messagebox.showinfo(
        "Buy Tickets", 
        f"Ticket Booking Form for: {movie_title}\n\n"
        "Features here will include:\n"
        "- Customer Name & Contact Entry\n"
        "- Ticket Type Selection (Adult/Concession)\n"
        "- Availability & Inventory Validation"
    )

def create_app():
    root = tk.Tk()
    root.movie_images = []
    root.title("Movies4Us Ticket Management System")
    root.geometry("900x700")
    root.configure(bg='#f8f9fa')

    header_frame = tk.Frame(root, bg="#2b2d42", height=70, padx=20, pady=10)
    header_frame.pack(fill="x", side="top")

    title_label = tk.Label(
        header_frame,
        text="🎬 Movies4Us",
        font=("Helvetica", 22, "bold"),
        fg="#ffffff",
        bg="#2b2d42"
    )
    title_label.pack(side="left")

    subtitle_label = tk.Label(
        header_frame,
        text="Melbourne Ticket Management System",
        font=("Helvetica", 10, "italic"),
        fg="#8d99ae",
        bg="#2b2d42"
    )
    subtitle_label.pack(side="left", padx=15)

    staff_login_btn = tk.Button(
        header_frame,
        text="🔐 Staff Login",
        font=("Helvetica", 10, "underline"),
        fg="#4cc9f0",
        bg="#2b2d42",
        bd=0,
        activebackground="#2b2d42",
        activeforeground="#ffffff",
        cursor="hand2",
        command=open_staff_login
    )
    staff_login_btn.pack(side="right")

    content_frame = tk.Frame(root, bg="#f8f9fa", padx=20, pady=20)
    content_frame.pack(fill="both", expand=True)

    section_heading = tk.Label(
        content_frame,
        text="Now Showing - Choose a Movie",
        font=("Helvetica", 16, "bold"),
        bg="#f8f9fa",
        fg="#2b2d42"
    )
    section_heading.pack(anchor="w", pady=(0, 15))

    grid_container = tk.Frame(content_frame, bg="#f8f9fa")
    grid_container.pack(fill="both", expand=True)

    grid_container.columnconfigure(0, weight=1)
    grid_container.columnconfigure(1, weight=1)

    for index, movie in enumerate(movies):
        row = index // 2
        col = index % 2

        card = tk.LabelFrame(
            grid_container,
            bg="#ffffff",
            bd=1,
            relief="solid",
            padx=12,
            pady=12
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        card.columnconfigure(1, weight=1)

        IMAGE_FOLDER = "images"
        img_path = os.path.join(IMAGE_FOLDER, movie["image"])

        try:
            photo = tk.PhotoImage(file=img_path)
            root.movie_images.append(photo)

            poster_label = tk.Label(card, image=photo, bg="#ffffff")
            poster_label.grid(row=0, column=0, rowspan=4, padx=(0, 15), sticky="nw")
        except Exception:
            fallback_lbl = tk.Label(card, text="[Poster\nMissing]", width=12, height=8, bg="#e9ecef", fg="#6c757d", font=("Helvetica", 9))
            fallback_lbl.grid(row=0, column=0, rowspan=4, padx=(0, 15), sticky="nw")

        m_title = tk.Label(
            card,
            text=movie["title"],
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
            anchor="w"
        )
        m_title.grid(row=0, column=1, sticky="w")

        m_genre = tk.Label(
            card,
            text=f"genre: {movie['genre']}",
            font=("Helvetica", 9),
            fg="#555555",
            bg="#ffffff",
            anchor="w"
        )
        m_genre.grid(row=1, column=1, sticky="w")

        m_rating = tk.Label(
            card,
            text=f"Rating: {movie['rating']}",
            font=("Helvetica", 9, "bold"),
            fg="#2a9d8f",
            bg="#ffffff",
            anchor="w"
        )
        m_rating.grid(row=2, column=1, sticky="w", pady=(0, 10))

        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.grid(row=3, column=1, sticky="ew")

        info_btn = tk.Button(
            btn_frame,
            text="Info",
            font=("Helvetica", 9),
            bg="#e9ecef",
            relief="groove",
            cursor="hand2",
            command=lambda m=movie["title"]: show_movie_info(m)
        )
        info_btn.pack(side="left", padx=(0, 15))

        session_btn = tk.Button(
            btn_frame,
            text="Sessions",
            font=("Helvetica", 9),
            bg="#e9ecef",
            relief="groove",
            cursor="hand2",
            command=lambda m=movie["title"]: show_session_times(m)
        )
        session_btn.pack(side="left", padx=(0, 15))

        buy_btn = tk.Button(
            btn_frame,
            text="🎟️ Buy Tickets",
            font=("Helvetica", 9, "bold"),
            bg="#4361ee",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=lambda m=movie["title"]: buy_tickets(m)
        )
        buy_btn.pack(side="left")
    footer = tk.Label(
        root,
        text="Movies4Us Pty Ltd © 2026 - Staff Operational & Ticket Management Portal",
        font=("Helvetica", 8),
        bg="#2b2d42",
        fg="#8d99ae",
        pady=5
    )
    footer.pack(fill="x", side="bottom")
    return root

if __name__ == "__main__":
    app = create_app()
    app.mainloop()