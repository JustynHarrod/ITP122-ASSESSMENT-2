import backend

def check_availability(movie_title, quantity):        # TODO: Check backend.MOVIES_DATA for remaining tickets
       if movie_title not in backend.MOVIES_DATA["title"]:
              return "Error: No movie exist"

       available_seats = backend.MOVIES_DATA["title"]["tickets_remaining"]
       return True, "Seats available"

def record_sale(sale_data):        # TODO: Append to backend.SALES_HISTORY list
       return True

print(backend.MOVIES_DATA[1]["title"]["tickets_remaining"])



