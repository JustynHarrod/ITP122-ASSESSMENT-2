

import tkinter



window = tkinter.Tk()
window.title("login form")
window.geometry("640x750")


#creating widgets
login_label = tkinter.Label(window, text="STAFF LOGIN PAGE:", bg="blue", fg="white", font=("Arial", 45))
username_label = tkinter.Label(window, text="Username:", font=("Arial", 16))
username_entry = tkinter.Entry(window, font=("Arial", 16))
password_entry = tkinter.Entry(window, show="*", font=("Arial", 16))
password_label = tkinter.Label(window, text="Password:", font=("Arial", 16))
login_button = tkinter.Button(window, text="Login",fg="black", bg="pink", font=("Arial", 16), command=lambda: check_login(username_entry.get(), password_entry.get()))


#placing widgets on the window
login_label.grid(row=0, column=0, columnspan=2,sticky="news")
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=3, sticky="news")




window.mainloop()
