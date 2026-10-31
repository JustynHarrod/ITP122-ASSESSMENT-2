#import staff credentials from backend
from backend import*
#thi is for GUI login UN and PW and return true or false 
def verify_staff_login(username,
password):
    return (
        username in
STAFF_CREDENTIALS
        and
STAFF_CREDENTIALS[username] ==
password
    )

#staff input credentials they have three attempts this only works in the terminal ATM yet to implement GUI
def staff_login():
    for attempt in range(3):
        username = input("Enter " \
        "your username ").strip()
        password = input("Enter your " \
        "password")
#if credentials are correct a welcome with there name and a successful print are returned
        if (
            username in
STAFF_CREDENTIALS
            and
STAFF_CREDENTIALS[username] ==
password            
        ):
            print("Welcome,",
username)
            print("login successful!")
            return True 
#if a failed attempt is detected a please try again will show and how many attempts out of 3 are remaining
        else:
            print("Invalid " \
            "username or password detected please try again.")
        print ("Attempts " \
        "remaining:",  2 - attempt)
#or else the loop loop finishes with to many unsuccessful attempts please try again
    else:
        print("Too many " \
        "unsucccessful attempts program " \
        "ended please try again.")
    return False



staff_login()            
            
              

  


