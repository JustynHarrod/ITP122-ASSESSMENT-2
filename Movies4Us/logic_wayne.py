from backend import*

def staff_login():
    for attempt in range(3):
        username = input("Enter " \
        "your username ").strip()
        password = input("Enter your " \
        "password")

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
            

        else:
            print("Invalid  \
username, or password please try again.")
        print ("Attempts " \
        "remaining:",  2 - attempt)

    else:
        print("Too many " \
        "unsucccessful attempts program " \
        "ended.")
    return False



staff_login()            
            
              

  


