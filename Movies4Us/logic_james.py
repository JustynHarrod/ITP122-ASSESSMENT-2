from datetime import datetime
import backend

def process_payment(card_num, expiry, cvv):


#Accounting for edge cases in which users add spaces when entering a space in the card number entry field
    card_num = card_num.replace(" ", "")

#Checking digits of card number

    if len(card_num) != 16 or not card_num.isdigit():
       return False, "Invalid Card Number"


#Accounting for edge cases in which users add a "/" when entering their card expiry
    expiry = expiry.replace("/", "")

#Checking digits of expiry
    
    if len(expiry) != 4 or not expiry.isdigit():
       return False, "Invalid Expiry"


#Creating variables for ease of use

    expiry_year = int(expiry[2:]) + 2000
    expiry_month = int(expiry[:2])
    current_year = datetime.now().year
    current_month = datetime.now().month

#Checking if the card is in date, if the expiry is too far in the future then it will be invalid as most cards expire every 2-3 years, though gift cards can last 10 occasionally

    if expiry_year < current_year or expiry_year > current_year + 11 or expiry_month > 12 or expiry_month < 1:
        
        return False, "Invalid Expiry"

#Only checking the month if the expiry year is equal to current year, range checking the entered expiry month to ensure it is a valid entry

    elif expiry_year == current_year:
        if not expiry_month >= current_month :
            return False, "Invalid Expiry"


    

#Checking digits of CVV
    
    if len(cvv) != 3 or not cvv.isdigit():
       return False, "Invalid CVV"
    
    else:
       return True, "Payment Approved"

 # TODO: Deduct quantity from backend.MOVIES_DATA

def update_inventory(movie_title, quantity, requested_session):  
    movie = next((m for m in backend.MOVIES_DATA if m["title"] == movie_title), None)
    if movie is None:
       return False, f"Error updating inventory, {movie_title} not found."

    session = next((s for s in movie["sessions"] if s["session_id"] == requested_session), None)

    if session is None:
           return False, f"Error updating inventory, {requested_session} not found."

    session["tickets_remaining"] -= quantity

    return True, "Inventory successfully updated"