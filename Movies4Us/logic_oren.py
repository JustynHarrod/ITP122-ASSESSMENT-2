import backend

def check_availability(movie_title, requested_seats):
       movie = None
       for m in backend.MOVIES_DATA:
           if m.get('title', "") == movie_title.lower().strip():
                     m = movie
                     break

       if movie is None:
              return False, "Error: No movie exist"

       if requested_seats > movie['tickets_remaining']:
              return False, "Error: The movie doesn't have enough seats available."
       
       return True, "Seats available"

print(check_availability("Street Fighter", 50))
print(check_availability("Avatar", 50))

def record_sale(sale_data):
       return True