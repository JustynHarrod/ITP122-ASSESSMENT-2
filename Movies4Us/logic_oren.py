import backend

# def for check_availability is project.
def check_availability(movie_title, requested_seats):
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

def record_sale(sale_data, quantity):
       for p in backend.SALES_HISTORY:
              if p.get ("type", "").lower().strip() == sale_data.lower().strip():
                     return backend.PRICES[sale_data.strip().title()] * quantity
       else:
              print("Sale not Found")
       return None
price = record_sale("Adult", 5)
print (f"Price of ticket: {price:.2f}")