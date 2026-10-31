#Building a customer UI window to be called upon by main.py
#Allows customer to select how many tickets they would like and then continue to payment
#Essentially hoyts checkout section that pops up after the seat selection area

import customtkinter as ctk
import backend
import sys
from logic_james import process_payment
print("Customer UI file started")

#Super basic window
class CustomerUI(ctk.CTkToplevel):
    def __init__(self, master, movie_title="Unknown movie", session_time="No session selected"):
        super().__init__(master)
        self.movie_title = movie_title
        self.session_time = session_time
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

        # Movie and session chosen on the main screen
        self.session_label = ctk.CTkLabel(
            self,
            text=f"{self.movie_title}  |  Session: {self.session_time}",
            font=("Arial", 16, "bold"),
            text_color="#f59e0b"
        )
        self.session_label.pack(pady=(0, 15))

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

        #Checkout total
        self.total_label = ctk.CTkLabel(
            self,
            text="Total: $0.00",
            font=("Arial", 22, "bold"),
            text_color="#ffffff"
        )
        self.total_label.pack(pady=25)
#Continue payment button, cannot be used until customer select ticket
        self.continue_button = ctk.CTkButton(
            self,
            text="Continue to Payment",
            width=220,
            height=45,
            font=("Arial", 16, "bold"),
            state="disabled",
            command=self.continue_to_payment
        )
        self.continue_button.pack(pady=15)

#Payment screen container
        self.payment_frame = ctk.CTkFrame(
            self,
            fg_color="#1a1d24",
            corner_radius=12
        )

#Hide payment screen until customer continues
        self.payment_frame.pack_forget()

#Payment heading
        self.payment_heading = ctk.CTkLabel(
            self.payment_frame,
            text="Payment Details",
            font=("Arial", 26, "bold"),
            text_color="#ffffff"
        )
        self.payment_heading.pack(pady=(25, 15))

#Order Summary
        self.order_summary = ctk.CTkLabel(
            self.payment_frame,
            text="Your Order Will Appear Here",
            font=("Arial", 16),
            text_color="#a1a1aa",
            justify="left"
        )
        self.order_summary.pack(pady=20)

#Card Number
        self.card_number_entry = ctk.CTkEntry(
            self.payment_frame,
            placeholder_text="Card Number",
            width=350,
            height=40
        )
        self.card_number_entry.pack(pady=10)

#Expiry date
        self.expiry_entry = ctk.CTkEntry(
            self.payment_frame,
            placeholder_text="Expiry Date (MMYY)",
            width=350,
            height=40
        )
        self.expiry_entry.pack(pady=10)

#CVV
        self.cvv_entry = ctk.CTkEntry(
            self.payment_frame,
            placeholder_text="CVV",
            width=350,
            height=40,
            show="*"
        )
        self.cvv_entry.pack(pady=10)

#Back to ticket selection
        self.back_button = ctk.CTkButton(
            self.payment_frame,
            text="Back to Tickets",
            width=160,
            command=self.back_to_tickets
        )
        self.back_button.pack(pady=10)

#Pay now button
        self.pay_button = ctk.CTkButton(
            self.payment_frame,
            text="Pay Now",
            width=220,
            height=45,
            font=("Arial", 16, "bold"),
            text_color="#ffffff",
            command=self.make_payment
        )
        self.pay_button.pack(pady=15)

#payment checker
        self.payment_result = ctk.CTkLabel(
            self.payment_frame,
            text="",
            font=("Arial", 14),
            text_color="#ffffff"
        )
        self.payment_result.pack(pady=10)

#making the payment
    def make_payment(self):

#retrieve card details
        card_number = self.card_number_entry.get()
        expiry = self.expiry_entry.get()
        cvv = self.cvv_entry.get()

#process payment
        approved, message = process_payment(
            card_number,
            expiry,
            cvv
        )

        if approved:
            self.payment_result.configure(
                text="Payment Successful!",
                text_color="#4ade80"
            )
        else:
            self.payment_result.configure(
                text=message,
                text_color="#ef4444"
            )


#Create functionality for back button
    def back_to_tickets(self):

        #Hide payment screen
        self.payment_frame.pack_forget()

        #Show ticket screen
        self.heading.pack(pady=(30, 5))
        self.subtitle.pack(pady=(0, 25))
        self.session_label.pack(pady=(0, 15))
        self.ticket_frame.pack(fill="x", padx=100, pady=10)
        self.total_label.pack(pady=25)
        self.continue_button.pack(pady=15)

#Calculating total

    def update_total(self):
        total = sum(
            self.ticket_quantities[ticket_type] * price
            for ticket_type, price in backend.PRICES.items()
        )

        self.total_label.configure(
            text=f"Total: ${total:.2f}"
        )

#check ticket quantities before allowing continuation

    def update_continue_button(self):
        total_tickets = sum(self.ticket_quantities.values())

        if total_tickets > 0:
            self.continue_button.configure(state="normal")
        else:
            self.continue_button.configure(state="disabled")



#continue to payment function

    def continue_to_payment(self):
        #build order summary

        summary = f"YOUR ORDER\n\n{self.movie_title} - {self.session_time}\n\n"

        for ticket_type, quantity in self.ticket_quantities.items():
            if quantity > 0:
                price = backend.PRICES[ticket_type]
                subtotal = quantity * price

                summary += f"{ticket_type}: {quantity} x ${price:.2f} = ${subtotal:.2f}\n"

        summary += f"\n{self.total_label.cget('text')}"

        self.order_summary.configure(text=summary)

        #hide ticket selection screen
        self.heading.pack_forget()
        self.subtitle.pack_forget()
        self.session_label.pack_forget()
        self.ticket_frame.pack_forget()
        self.continue_button.pack_forget()
        self.total_label.pack_forget()

        #Dispaly payment screen
        self.payment_frame.pack(
            fill="x",
            padx=100,
            pady=10
        )













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
        self.update_total()
        self.update_continue_button()

    def remove_ticket(self, ticket_type):
        if self.ticket_quantities[ticket_type] > 0:
            self.ticket_quantities[ticket_type] -= 1

        self.refresh_ticket_row(ticket_type)
        self.update_total()
        self.update_continue_button()

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
    # main.py passes the movie title and session time as command-line arguments.
    movie_title = sys.argv[1] if len(sys.argv) > 1 else "Unknown movie"
    session_time = sys.argv[2] if len(sys.argv) > 2 else "No session selected"

    app = ctk.CTk()
    app.withdraw()

    customer_window = CustomerUI(app, movie_title, session_time)
    # Closing the checkout window should also end the hidden root window.
    customer_window.protocol("WM_DELETE_WINDOW", app.destroy)

    app.mainloop()