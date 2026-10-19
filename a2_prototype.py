# ============================================================
# Movies4Us Ticket Management System - GUI Prototype
# ------------------------------------------------------------
# This is a prototype of the customer-facing home screen.
# It shows a grid of "Now Showing" movies. Each movie has three
# buttons (Info, Sessions, Buy Tickets). At this stage the buttons
# only pop up placeholder message boxes - the real features
# (booking form, staff login, reports) will be built later.
# ============================================================
 
# tkinter is Python's built-in library for making windows and buttons (a GUI)

import tkinter as tk

# ttk gives "themed" widgets, messagebox gives us simple popup windows

from tkinter import ttk, messagebox

# os lets us build file paths that work on any operating system

import os

# ------------------------------------------------------------
# MOVIE DATA
# ------------------------------------------------------------
# A list of dictionaries. Each dictionary is one movie, with its
# title, genre, age rating and the file name of its poster image.
# To add a new movie to the screen, just add another dictionary here -
# the loop further down builds a card for every item automatically.

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


# ------------------------------------------------------------
# BUTTON FUNCTIONS
# ------------------------------------------------------------
# Each function below runs when its matching button is clicked.
# For now they show a popup (messagebox.showinfo) describing what
# the real feature will do. These are the "placeholders" to replace
# when we build the full system.

def open_staff_login():
    """Handles staff login link click."""
    
    # showinfo(window title, message text). "\n" starts a new line.
    
    messagebox.showinfo("Staff Login", "Staff Login modal will open here. \n\nThis will grant access to logical module 2: Operational reports.")

def show_movie_info(movie_title):
    """Displays movie details."""
    
    # movie_title is passed in so the popup names the correct movie
    
    messagebox.showinfo("Movie Info", f"Detailed synopsis, director, and cast info for: \n\n🎥 {movie_title}")

def show_session_times(movie_title):
    """Displays available screening sessions."""
    
    # Hard-coded example times for the prototype (same for every movie)
    
    sessions = "• Today: 1:30 PM, 4:45 PM, 7:15 PM, 9:30 PM"
    messagebox.showinfo("Session Times", f"Screening Schedule for {movie_title}:\n\n{sessions}")

def buy_tickets(movie_title):
    """Triggers the ticket purchase flow (Logical Module 1)."""
    
    # Lists the features the real booking form will need to include
    
    messagebox.showinfo(
        "Buy Tickets", 
        f"Ticket Booking Form for: {movie_title}\n\n"
        "Features here will include:\n"
        "- Customer Name & Contact Entry\n"
        "- Ticket Type Selection (Adult/Concession)\n"
        "- Availability & Inventory Validation"
    )

# ------------------------------------------------------------
# MAIN WINDOW BUILDER
# ------------------------------------------------------------
# This function builds the whole screen and returns the window.
# The screen is made of layers: Header (top), Content (middle),
# Footer (bottom).

def create_app():
    
    # Create the main application window ("root")
    
    root = tk.Tk()
    
    # Keep a list of poster images on the window itself. tkinter
    # deletes images that aren't stored somewhere, so without this
    # the posters would disappear.
    
    root.movie_images = []
    root.title("Movies4Us Ticket Management System")
    root.geometry("900x700")                    # window size: width x height in pixels
    root.configure(bg='#f8f9fa')              # light grey background

# ---------------- HEADER (dark bar at the top) ----------------
    # A Frame is an invisible container used to group widgets together
    
    header_frame = tk.Frame(root, bg="#2b2d42", height=70, padx=20, pady=10)
    header_frame.pack(fill="x", side="top") # stretch across the full width

    # Logo / business name on the left

    title_label = tk.Label(
        header_frame,
        text="🎬 Movies4Us",
        font=("Helvetica", 22, "bold"),
        fg="#ffffff",                           # fg = text colour
        bg="#2b2d42"                            # bg = background colour
    )
    title_label.pack(side="left")

    # Smaller italic tagline next to the logo

    subtitle_label = tk.Label(
        header_frame,
        text="Melbourne Ticket Management System",
        font=("Helvetica", 10, "italic"),
        fg="#8d99ae",
        bg="#2b2d42"
    )
    subtitle_label.pack(side="left", padx=15)
    
    # Staff login button on the right. It's styled like a link
    # (underlined, no border) so it stays out of the customers' way.

    staff_login_btn = tk.Button(
        header_frame,
        text="🔐 Staff Login",
        font=("Helvetica", 10, "underline"),
        fg="#4cc9f0",
        bg="#2b2d42",
        bd=0, # no border
        activebackground="#2b2d42",             # colours while the mouse is pressing it
        activeforeground="#ffffff",
        cursor="hand2",                           # mouse turns into a pointing hand
        command=open_staff_login                  # function to run on click
    )
    staff_login_btn.pack(side="right")

    # ---------------- MAIN CONTENT AREA ----------------

    content_frame = tk.Frame(root, bg="#f8f9fa", padx=20, pady=20)
    content_frame.pack(fill="both", expand=True) # fill all the leftover space


    # Heading above the movie grid
    
    section_heading = tk.Label(
        content_frame,
        text="Now Showing - Choose a Movie",
        font=("Helvetica", 16, "bold"),
        bg="#f8f9fa",
        fg="#2b2d42"
    )
    section_heading.pack(anchor="w", pady=(0, 15)) # anchor="w" = align left


    # Container that holds the movie cards in a grid layout
    
    grid_container = tk.Frame(content_frame, bg="#f8f9fa")
    grid_container.pack(fill="both", expand=True)
    
    # Two equal-width columns (weight=1 means they share space evenly)
    
    grid_container.columnconfigure(0, weight=1)
    grid_container.columnconfigure(1, weight=1)

    # ---------------- MOVIE CARDS ----------------
    # Loop through the movies list. enumerate() gives us the position
    # (index 0, 1, 2, 3) as well as the movie itself.

    for index, movie in enumerate(movies):
        
        # Work out where this card goes in the 2-column grid:
        # index 0 -> row 0, col 0 | index 1 -> row 0, col 1
        # index 2 -> row 1, col 0 | index 3 -> row 1, col 1
        
        row = index // 2                            # // is whole-number division
        col = index % 2                             # % is the remainder

        # The "card": a white box with a border holding one movie's details
        
        card = tk.LabelFrame(
            grid_container,
            bg="#ffffff",
            bd=1,
            relief="solid",
            padx=12,
            pady=12
        )
        
        # sticky="nsew" makes the card stretch to fill its grid cell
        
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Let column 1 of the card (the text side) stretch to fill space
        
        card.columnconfigure(1, weight=1)

        # Poster image: look for the file inside the "images" folder.
        # (The "images" folder must sit next to this script.)
        
        IMAGE_FOLDER = "images"
        img_path = os.path.join(IMAGE_FOLDER, movie["image"])


        # try/except: if the image loads, show it. If anything goes
        # wrong (file missing, wrong format), show a grey placeholder
        # instead so the program doesn't crash.
        
        try:
            photo = tk.PhotoImage(file=img_path)
            root.movie_images.append(photo)                             # store it so it isn't deleted

            poster_label = tk.Label(card, image=photo, bg="#ffffff")
            
            # Poster sits in column 0 and spans all 4 rows on the left
            
            poster_label.grid(row=0, column=0, rowspan=4, padx=(0, 15), sticky="nw")
        except Exception:
            fallback_lbl = tk.Label(card, text="[Poster\nMissing]", width=12, height=8, bg="#e9ecef", fg="#6c757d", font=("Helvetica", 9))
            fallback_lbl.grid(row=0, column=0, rowspan=4, padx=(0, 15), sticky="nw")

        # Movie title (row 0, right of the poster)
        
        m_title = tk.Label(
            card,
            text=movie["title"],
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
            anchor="w"
        )
        m_title.grid(row=0, column=1, sticky="w")

        # Movie genre (row 1)
        
        m_genre = tk.Label(
            card,
            text=f"Genre: {movie['genre']}",
            font=("Helvetica", 9),
            fg="#555555",
            bg="#ffffff",
            anchor="w"
        )
        m_genre.grid(row=1, column=1, sticky="w")
        
        # Age rating in green (row 2), with extra space below it
        
        m_rating = tk.Label(
            card,
            text=f"Rating: {movie['rating']}",
            font=("Helvetica", 9, "bold"),
            fg="#2a9d8f",
            bg="#ffffff",
            anchor="w"
        )
        m_rating.grid(row=2, column=1, sticky="w", pady=(0, 10))

        # A small frame to hold the three buttons side by side (row 3)
        
        btn_frame = tk.Frame(card, bg="#ffffff")
        btn_frame.grid(row=3, column=1, sticky="ew")

        # NOTE on "lambda m=movie['title']: ...":
        # Each button needs to remember WHICH movie it belongs to.
        # The lambda saves the current movie's title in "m" at the time
        # the button is created. Without the "m=" part, every button
        # would end up using the last movie in the loop.
 
        # "Info" button -> shows movie details popup

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

        # "Sessions" button -> shows session times popup
        
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

        # "Buy Tickets" button -> blue and bold so it stands out as the
        # main action. Opens the ticket booking placeholder.
        
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
        
    # ---------------- FOOTER (dark bar at the bottom) ----------------
    
    footer = tk.Label(
        root,
        text="Movies4Us Pty Ltd © 2026 - Staff Operational & Ticket Management Portal",
        font=("Helvetica", 8),
        bg="#2b2d42",
        fg="#8d99ae",
        pady=5
    )
    footer.pack(fill="x", side="bottom")
    
    # Hand the finished window back to whoever called create_app()
    
    return root

# ------------------------------------------------------------
# PROGRAM ENTRY POINT
# ------------------------------------------------------------
# This only runs when the file is run directly (not when imported
# into another file). It builds the window, then mainloop() keeps
# it open and listening for clicks until the user closes it.

if __name__ == "__main__":
    app = create_app()
    app.mainloop()