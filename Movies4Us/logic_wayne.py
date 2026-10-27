from backend import *
username = input("Enter your username: ")
password = input("Enter your password: ")

if username in STAFF_CREDENTIALS and STAFF_CREDENTIALS[username] == password:
    print("Login successful!")
else:
    print("Invalid username or password. Please try again.")