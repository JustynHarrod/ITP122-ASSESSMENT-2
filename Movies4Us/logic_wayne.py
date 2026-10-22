import tkinter
frame = tkinter.Tk()
frame.title("login form")
frame.geometry("340x440")
frame.configure(bg="blue")

frame = tkinter.Frame()


#creating widgets
login_label = tkinter.Label( text="MOVIES4US LOGIN:", bg="black", fg="white", font=("Arial", 45))
username_label = tkinter.Label(frame, text="Username:", font=("Arial", 16))
username_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
password_label = tkinter.Label(frame, text="Password:", font=("Arial", 16))
login_button = tkinter.Button(frame, text="Login",fg="black", bg="pink", font=("Arial", 16), command=lambda: check_login(username_entry.get(), password_entry.get()))


#placing widgets on the window
login_label.grid(row=0, column=0, columnspan=2,sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=3, sticky="news")

frame.pack()


frame.mainloop()
