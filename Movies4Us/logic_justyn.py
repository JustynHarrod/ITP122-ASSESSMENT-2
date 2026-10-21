import backend

def generate_sales_report():
       sales = 0
       for sale in backend.SALES_HISTORY:
              sales += sale["amount"]
              revenue = calculate_revenue()
       if revenue > 0 and sales > 0:
              average = revenue / sales
       else:
              average = 0
       most_sold = 0
       least_sold = 0
       for movie in backend.MOVIES_DATA:
              sold = movie["capacity"] - movie["tickets_remaining"]
              if sold > most_sold:
                     most_sold = sold
              if least_sold is None or sold < least_sold:
                     least_sold = sold
       top_movies = []
       lowest_movies = []
       for movie in backend.MOVIES_DATA:
              sold = movie["capacity"] - movie["tickets_remaining"]
              if sold == most_sold:
                     top_movies.append(movie["title"])
              if sold == least_sold:
                     lowest_movies.append(movie["title"])
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
       total = 0
       for sale in backend.SALES_HISTORY:
           price = backend.PRICES[sale["type"]]
           total += price * sale["amount"]      
       return total

print(generate_sales_report())