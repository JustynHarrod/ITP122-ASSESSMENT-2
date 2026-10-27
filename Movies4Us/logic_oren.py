from backend import *
import backend

# def for check_availability for project.
def check_availability(movie_title, requested_session, requested_seats):
       """The Function checks availability for movie, the session and then seats, print(check_availability("Movie", 104 session, 50 seats)).      
       Returns back with print with message. """
       # for loop to check backend.MOVIES_DATA for titles to check if title exists.
       movie = None
       for m in MOVIES_DATA:
              if m["title"] == movie_title:
                     movie = m
                     break
       if movie is None:
              return False ## f"Error: {movie_title} doesn't exist in backend data."
       session = None
       for s in movie["sessions"]:
              if s["session_id"] == requested_session:
                     session = s
                     break
       # backup if movie doesn't exist.
       if session is None:
              return False ## f"Error: Session {requested_session}, not available for {movie_title}"
       # if users requests 80 seats for and it's more than what remains it will tell users that not enough seats.
       if requested_seats > session["tickets_remaining"]:
              return False ## f"Error: {movie_title} doesn't have enough seats available."
       # if users requests seat and they are availble.
       if requested_seats <= session["tickets_remaining"]:
              return True ## f"Seats available for {movie_title} in {requested_session}."

print(check_availability("Street Fighter", 104, 50))
print(check_availability("The Odyssey", 801, 50))
print(check_availability("Street Fighter", 140, 50))
print(check_availability("Avatar", 154, 50))

# def for sale_data for project.
def record_sale(sale_data, quantity):
       """Function gives specified ticket price for each category, "Adult", 5 tickets = $75.00 
        Returns Price of ticket. """
       # for loop to check p = price in sales history.
       for p in SALES_HISTORY:
              if p.get ("type", "").lower().strip() == sale_data.lower().strip():
                     return PRICES[sale_data.strip().title()] * quantity
       # runs if it cannot find sale type.
       print("Sale not found")
       return None

# call to price to test.
price = record_sale("test", 5)
price_adult = record_sale("adult", 2)
price_child = record_sale("child", 1000)
price_concession = record_sale("concession", 10)
if price is not None:
       print (f"Price of ticket: ${price:.2f}") 

print(f"Adult tickets: ${price_adult:,.2f}")
print(f"Child tickets: ${price_child:,.2f}")
print(f"Concession tickets: ${price_concession:,.2f}")
