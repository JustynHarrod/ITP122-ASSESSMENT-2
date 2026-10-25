import customtkinter as ctk
import backend, logic_justyn

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MetricCard(ctk.CTkFrame):
    """Reusable card for displaying top level metrics (Sales, Revenue, etc.)."""
    def __init__(self, master, title, value, subtitle=""):
        super().__init__(master, fg_color="#1a1d24", corner_radius=10)
        self.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(self, text=title, font=("Arial", 12), text_color="#8a93a0")
        self.title_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 0))
        self.value_label = ctk.CTkLabel(self, text=str(value), font=("Arial", 24, "bold"), text_color="#ffffff")
        self.value_label.grid(row=1, column=0, sticky="w", padx=15, pady=(5, 0))

        if subtitle:
            self.sub_label = ctk.CTkLabel(self, text=subtitle, font=("Arial", 11), text_color="#6c757d")
            self.sub_label.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 15))
        else:
            self.configure(height=100)

class StaffDashboardWindow(ctk.CTk):
    """Standalone Staff Dashboard Window using grid layout"""
    def __init__(self):
        super().__init__()
        self.title("Movies4Us - Staff Portal")
        self.geometry("1280x900")
        self.configure(fg_color="#0f1117")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.report_data = logic_justyn.generate_sales_report()
        self.create_header()
        self.create_metrics_grid()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(30, 20))
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(header_frame, text="Staff Portal", font=("Arial", 26, "bold"), text_color="#ffffff")
        subtitle = ctk.CTkLabel(header_frame, text=("Access ticket sales, availability reports, and cinema performance."), font=("Arial", 13), text_color="#8a93a0",)
        subtitle.grid(row=1, column=0, sticky="w", pady=(5, 0))

    def create_metrics_grid(self):
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.grid(row=1, column=0, sticky="new", padx=40, pady=10)
        grid_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
        
        card_sold = MetricCard(grid_frame, title="Tickets Sold", value=self.report_data["total_sales"], subtitle="Across Sample Screenings",)
        card_sold.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        formatted_revenue = f"${self.report_data['revenue']:,.0f}"
        card_rev = MetricCard(grid_frame, title="Ticket Revenue", value=formatted_revenue, subtitle=f"Avg: ${self.report_data['average_ticket_price']:.2f}",)
        card_rev.grid(row=0, column=1, sticky="ew", padx=10)

        top_str = (
            ", ".join(self.report_data["top_movies"])
            if self.report_data["top_movies"]
            else "N/A"
        )
        card_top = MetricCard(grid_frame, title="Top Selling", value=top_str, subtitle="Best Performer")
        card_top.grid(row=0, column=2, sticky="ew", padx=10)

        low_str = (
            ", ".join(self.report_data["lowest_movies"])
            if self.report_data["lowest_movies"]
            else "N/A"
        )
        card_low = MetricCard(grid_frame, title="Lowest Performing", value=low_str, subtitle="Needs Attention",)
        card_low.grid(row=0, column=3, sticky="ew", padx=(10, 0))

if __name__ == "__main__":
    app = StaffDashboardWindow()
    app.mainloop()
        