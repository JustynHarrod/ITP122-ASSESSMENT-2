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
            padx=100,
            pady=10
        )

        #Allow the ticket rows to expand
        self.ticket_frame.grid_columnconfigure(0, weight=1)

        for row, (ticket_type, price) in enumerate(backend.PRICES.items()):
            self.create_ticket_row(ticket_type, price, row)

 #Create a row for each ticket type           
    def create_ticket_row(self, ticket_type, price, row):

    #Frame for ticket row
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
        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, minsize=100)
        row_frame.grid_columnconfigure(2, minsize=120)

        self.ticket_rows = getattr(self, "ticket_rows", {})
        self.ticket_rows[ticket_type] = row_frame

    #Ticket Name
        name_label = ctk.CTkLabel(
        row_frame,
        text=ticket_type,
        font=("Arial", 16, "bold"),
        text_color="#ffffff"
    )
        name_label.grid(
            row=0,
            column=0,
            sticky="w"
        )

    #Ticket price
        price_label = ctk.CTkLabel(
        row_frame,
        text=f"${price:.2f}",
        font=("Arial", 14),
        text_color="#a1a1aa"
    )
        price_label.grid(
            row=0,
            column=1,
            padx=15,
            sticky="e"
        )

    
    #Giving the controls their own frame for better looking formatting
        if not hasattr(self, "controls_frames"):
            self.controls_frames = {}

        controls_frames = ctk.CTkFrame(
            row_frame,
            fg_color="transparent"
        )
        controls_frames.grid(
            row=0,
            column=2,
            sticky="e"
        )
        self.controls_frames[ticket_type] = controls_frames

        #Create the add button
        self.refresh_ticket_row(ticket_type)




    #Quantity control
    def add_ticket(self, ticket_type):
        self.ticket_quantities[ticket_type] += 1
        self.refresh_ticket_row(ticket_type)

    def remove_ticket(self, ticket_type):
        if self.ticket_quantities[ticket_type] > 0:
            self.ticket_quantities[ticket_type] -= 1

        self.refresh_ticket_row(ticket_type)

    def refresh_ticket_row(self, ticket_type):
        controls_frame = self.controls_frames[ticket_type]
        quantity = self.ticket_quantities[ticket_type]
        

        #Get rid of old controls without getting rid of ticket name or price
        for widget in controls_frame.winfo_children():
            widget.destroy()

        if quantity == 0:
            #bring back the add button
            add_button = ctk.CTkButton(
                controls_frame,
                text = "Add",
                width = 90,
                command=lambda: self.add_ticket(ticket_type)
            )
            add_button.grid(row=0, column=0)

        else:
            #Show minus
            minus_button = ctk.CTkButton(
                controls_frame,
                text = "-",
                width=35,
                command=lambda: self.remove_ticket(ticket_type)
            )
            minus_button.grid(row=0, column=0, padx=2)

            #show quantity
            quantity_label = ctk.CTkLabel(
                controls_frame,
                text = str(quantity),
                width=30,
                font= ("Arial", 15, "bold")
            )
            quantity_label.grid(row=0, column=1, padx=2)

            #show plus button
            plus_button = ctk.CTkButton(
                controls_frame,
                text="+",
                width=35,
                command=lambda: self.add_ticket(ticket_type)
            )
            plus_button.grid(row=0, column=2, padx=2)













#Test loop to run Customer UI while I am building it
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()

    customer_window = CustomerUI(app)

    app.mainloop()