import backend

# def for check_availability for project.
def check_availability(movie_title, requested_seats):
       """Function checks availability for movie and seats, print(check_availability("Movie", 50 seats)). 
              
       Returns a True or false for seats.
       """
       movie = None
       # for loop to check if m = movie to check if title exists.
       for m in backend.MOVIES_DATA:
           if m.get("title", "").lower().strip() == movie_title.lower().strip():
                     movie = m
                     break
       # backup if movie doesn't exist.
       if movie is None:
              return False, f"Error: {movie_title} doesn't exist in backend data."
       # if users requests 80 seats for and it's more than what remains it will tell users that not enough seats.
       if requested_seats > movie["tickets_remaining"]:
              return False, f"Error: {movie_title} doesn't have enough seats available."
       # if users requests seat and they are availble.
       if requested_seats <= movie["tickets_remaining"]:
              return True, f"Seats available for {movie_title}."

print(check_availability("Street Fighter", 50))
print(check_availability("Avatar", 50))

# def for sale_data for project.
def record_sale(sale_data, quantity):
       """Function gives specified ticket price for each category, "Adult", 5 tickets = $75.00 
              
       Returns Price of ticket.
       """
       # for loop to check p = price in sales history.
       for p in backend.SALES_HISTORY:
              if p.get ("type", "").lower().strip() == sale_data.lower().strip():
                     return backend.PRICES[sale_data.strip().title()] * quantity
       # runs if it cannot find sale type.
       print("Sale not Found")
       return None

# call to price to test.
price = record_sale("test", 5)
price_adult = record_sale("adult", 2)
price_child = record_sale("child", 1000)
price_concession = record_sale("concession", 10)
if price is not None:
       print (f"Price of ticket: ${price:.2f}") 

print(f"Adult tickets: ${price_adult:.2f}")
print(f"Child tickets: ${price_child:.2f}")
print(f"Concession tickets: ${price_concession:.2f}")
