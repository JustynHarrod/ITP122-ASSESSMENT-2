import backend

def generate_sales_report():
       """Generates an aggregated sales report. 
       
       Returns a dictionary with total sales, total revenue, 
       average ticket price, and lists for top and lowest-selling movies.
       """
       tickets_sold = 0
       revenue = calculate_revenue()
       for sale in backend.SALES_HISTORY:
              tickets_sold += sale["amount"]
       # Prevent ZeroDivisionError if no sales have been recorded yet
       if revenue > 0 and tickets_sold > 0:
              average = revenue / tickets_sold
       else:
              average = 0
       most_sold = 0
       least_sold = None
       # First pass: determine the maximum and minimum ticket sales thresholds
       for movie in backend.MOVIES_DATA:
              sold = sum(
                     session["capacity"] - session["tickets_remaining"]
                     for session in movie["sessions"]
              )
              if sold > most_sold:
                     most_sold = sold
              if least_sold is None or sold < least_sold:
                     least_sold = sold
       top_movies = []
       lowest_movies = []
       # Second pass: capture all titles matching thresholds (handles multi-movie ties)
       for movie in backend.MOVIES_DATA:
              sold = sum(
                     session["capacity"] - session["tickets_remaining"]
                     for session in movie["sessions"]
              )
              if sold == most_sold:
                     top_movies.append(movie["title"])
              if sold == least_sold:
                     lowest_movies.append(movie["title"])
       # Fallback state if inventory has no movement
       if most_sold == 0:
              top_movies = []
              lowest_movies = []
       return {
              "total_sales": tickets_sold, 
              "revenue": revenue, 
              "average_ticket_price": average,
              "top_movies": top_movies,
              "lowest_movies": lowest_movies,
              }

def calculate_revenue():
       """Calculates total gross revenue from sales history.""" 
       total = 0
       for sale in backend.SALES_HISTORY:
           price = backend.PRICES[sale["type"]]
           total += price * sale["amount"]      
       return total

print(generate_sales_report())