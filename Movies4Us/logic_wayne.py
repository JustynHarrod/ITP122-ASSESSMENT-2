staff_credentials = {
    "wayne": "12345",
    "justyn": "123456",
    "james": "1234567",
    "oren": "12345678",
    "rob": "123456789"
}
username = input("Enter your username: ")
password = input("Enter your password: ")

if username in staff_credentials and staff_credentials[username] == password:
    print("Login successful!")
else:
    print("Invalid username or password. Please try again.")