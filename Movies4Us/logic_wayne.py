#vairables stored in backend are called upon with an import for staff credentials for login
from backend import *
STAFF_CREDENTIALS
#here user input of credentials they must match stored values for successfull login
#range gives the user 3 attempts to sucsessfully log in or the program will end
for attempt in range(3):
    username = input("Enter your " \
"username: ").strip()
    password = input("Enter your " \
"password: ")

#here if username and password match the loop will continue to the print function to a welcome successful login and break stopping the loop
#here else username and password do not match the loop will continue to the print function invalid un or pw please try again
#and else print the attempts remaining

    if (
        username in
STAFF_CREDENTIALS
        and
STAFF_CREDENTIALS[username] ==
password
    ):
         
         print("welcome,",
username)
         print("Login successful!")

         break
    else:
         print("Invalid username or password. please try again.")

         print("Attempts remaining:", 2 - attempt)

else:
     print("Too many unsuccessful"
 "attempts. program ended.")
              

  