import backend

def generate_sales_report():
       """Generates an aggregated sales report. 
       
       Returns a dictionary with total sales, total revenue, 
       average ticket price, and lists for top and lowest-selling movies.
       """
       sales = 0
       revenue = calculate_revenue()
       # Calculate total tickets sold
       for sale in backend.SALES_HISTORY:
              sales += sale["amount"]
       # Prevent ZeroDivisionError if no sales have been recorded yet
       if revenue > 0 and sales > 0:
              average = revenue / sales
       else:
              average = 0
       most_sold = 0
       least_sold = None
       # First pass: determine the maximum and minimum ticket sales thresholds
       for movie in backend.MOVIES_DATA:
              sold = movie["capacity"] - movie["tickets_remaining"]
              if sold > most_sold:
                     most_sold = sold
              if least_sold is None or sold < least_sold:
                     least_sold = sold
       top_movies = []
       lowest_movies = []
       # Second pass: capture all titles matching thresholds (handles multi-movie ties)
       for movie in backend.MOVIES_DATA:
              sold = movie["capacity"] - movie["tickets_remaining"]
              if sold == most_sold:
                     top_movies.append(movie["title"])
              if sold == least_sold:
                     lowest_movies.append(movie["title"])
       # Fallback state if inventory has no movement
       if most_sold == 0:
              top_movies = []
              lowest_movies = []
       return {
              "total_sales": sales, 
              "revenue": revenue, 
              "average_ticket_price": average,
              "top_movies": top_movies if top_movies else "No tickets sold yet",
              "lowest_movies": lowest_movies if lowest_movies else "No tickets sold yet",
              }

def calculate_revenue():
       """Calculates total gross revenue from sales history.""" 
       total = 0
       # Iterate through sales history to aggregate revenue per ticket type
       for sale in backend.SALES_HISTORY:
           price = backend.PRICES[sale["type"]]
           total += price * sale["amount"]      
       return total

print(generate_sales_report())