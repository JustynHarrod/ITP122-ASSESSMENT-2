import datetime
from datetime import datetime


def process_payment(card_num, expiry, cvv, amount, expiry_year, expiry_month, current_year, current_month):



#Checking digits of card number

    if len(card_num) != 16 or not card_num.isdigit():
       return False, "Invalid Card Number"

    else: 
        pass

#Checking digits of expiry
    
    if len(expiry) != 4 or not expiry.isdigit():
       return False, "Invalid Expiry"

    else:
        pass

#Creating variables for ease of use

    expiry_year = int(expiry[2:]) + 2000
    expiry_month = int(expiry[:2])
    current_year = datetime.now().year
    current_month = datetime.now().month

#Checking if the card is in date, if the expiry is too far in the future then it will be invalid as most cards expire every 2-3 years, though gift cards can last 10 occasionally

    if expiry_year < current_year or expiry_year > current_year + 11:
        return False, "Invalid Expiry"
        
    else:
        pass


    if not expiry_month >= current_month:
        return False, "Invalid Expiry"

    else:
        pass




#Checking digits of CVV
    
    if len(cvv) != 3 or not cvv.isdigit():
       return False, "Invalid CVV"
    
    else:
       return True, "Payment Approved"



def update_inventory(movie_title, quantity):
       # TODO: Deduct quantity from backend.MOVIES_DATA
       return True