        self.username_entry.pack(padx=15, pady=4)
        self.password_entry = ctk.CTkEntry(self.login_panel, placeholder_text="Password", show="•", width=220)
        self.password_entry.pack(padx=15, pady=4)
        self.login_error = ctk.CTkLabel(self.login_panel, text="", font=("Arial", 11), text_color="#ef4444")
        self.login_error.pack(padx=15, pady=(2, 0))
        ctk.CTkButton(self.login_panel, text="Login", fg_color="#f59e0b", hover_color="#915d04", text_color="#ffffff", width=220, command=self.attempt_staff_login).pack(padx=15, pady=(6, 12))
        self.username_entry.bind("<Return>", lambda e: self.attempt_staff_login())
        self.password_entry.bind("<Return>", lambda e: self.attempt_staff_login())
    def toggle_login_panel(self):
        """Shows the login panel if hidden, hides it if showing."""
        if self.login_visible:
            self.hide_login_panel()
        else:
            self.login_panel.place(relx=1, x=-40, y=70, anchor="ne")
            self.login_panel.lift()
            self.username_entry.focus()
            self.login_visible = True
    def hide_login_panel(self):
        """Hides the panel and clears anything typed in."""
        self.login_panel.place_forget()
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.login_error.configure(text="")
        self.login_visible = False
    def attempt_staff_login(self):
        """Checks the credentials, only open the staff screen if they are valid."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        if verify_staff_login(username, password):
            self.hide_login_panel()
            self.open_staff_portal()
        else:
            self.login_error.configure(text="Invalid username or password")
            self.password_entry.delete(0, "end")
    def open_staff_portal(self):
        """Opens the staff ui.py file (temp) until popout for staff login."""
        staff_ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "staff_ui.py")
        try:
            subprocess.Popen([sys.executable, staff_ui_path])
        except OSError as error:
            print(f"Could not open staff ui: {error}")

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()