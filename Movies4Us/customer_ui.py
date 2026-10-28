#Building a customer UI window to be called upon by main.py
#Allows customer to select how many tickets they would like and then continue to payment
#Essentially hoyts checkout section that pops up after the seat selection area

import customtkinter as ctk
import backend



#Super basic window
class CustomerUI(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
#Dictionary of default ticket quantities
        self.ticket_quantities = {
            "Adult": 0,
            "Child": 0,
            "Concession": 0
        }

        self.title("Movies4Us - Checkout")
        self.geometry("1280x900")
        self.configure(fg_color="#0f1117")

        # Main heading
        self.heading = ctk.CTkLabel(
            self,
            text="Movies4Us Checkout",
            font=("Arial", 28, "bold"),
            text_color="#ffffff"
        )
        self.heading.pack(pady=(30, 5))

        # Subtitle
        self.subtitle = ctk.CTkLabel(
            self,
            text="Select your tickets",
            font=("Arial", 15),
            text_color="#a1a1aa"
        )
        self.subtitle.pack(pady=(0, 25))

        # Container for ticket rows
        self.ticket_frame = ctk.CTkFrame(
            self,
            fg_color="#1a1d24",
            corner_radius=12
        )
        self.ticket_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )


def create_ticket_row(self, ticket_type, price, row):
    #Frame for this ticket row
    row_frame = ctk.CTkFrame(
        self.ticket_frame,
        fg_color="transparent"
    )
    row_frame.grid(
        row=row,
        column=0,
        sticky="ew",
        padx=20,
        pady=15
    )
    #Ticket Name
    name_label = ctk.CTkLabel(
        row_frame,
        text=ticket_type,
        font=("Arial", 16, "bold"),
        text_color="#ffffff"
    )
    name_label.pack(side="left")

    #Ticket price
    price_label = ctk.CTkLabel(
        row_frame,
        text=f"${price:.2f}",
        font=("Arial", 14),
        text_color="#a1a1aa"
    )
    price_label.pack(side="left", padx=15)

    #Add a button
    add_button = ctk.CTkButton(
        row_frame,
        text="Add",
        width=90
    )
    add_button.pack(side="right")
















#Test loop to run Customer UI while I am building it
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()

    customer_window = CustomerUI(app)

    app.mainloop()