from backend import *

def verify_staff_login(username, password):

    if username in STAFF_CREDENTIALS and STAFF_CREDENTIALS[username] == password:
        return True
        print("Login successful!")
    else:
        return False
        print("Invalid username or password. Please try again.")