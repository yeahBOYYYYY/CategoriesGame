from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from Client.Gui.Widgets.interactive_button import InterActiveButton
from Client.Gui.page_template import PageTemplate
from command import Command, CommandName


class SignupPage(PageTemplate):
    """
    Signup page of the application.
    """

    def __init__(self, window: "Window") -> None:
        """
        Initialize the signup page.
        :param window: The window of the application.
        """
        super().__init__(window)

        self.username: tk.StringVar = tk.StringVar()
        self.password: tk.StringVar = tk.StringVar()
        self.email: tk.StringVar = tk.StringVar()

        self.username_entry: ttk.Entry = ttk.Entry(self, textvariable=self.username)
        self.password_entry: ttk.Entry = ttk.Entry(self, textvariable=self.password)
        self.email_entry: ttk.Entry = ttk.Entry(self, textvariable=self.email)

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        # create page title
        self.create_text(600, 100, text="Signup", font=("Arial", 60, "bold", "underline"))

        # create the buttons
        submit_button = InterActiveButton(self, text="Submit", command=self.submit_signup_info)
        submit_button.place(x=300, y=600, width=600, height=98)

        home_button = InterActiveButton(self, text="Home", command=self.window.show_page("StartPage"), bg="#213c75")
        home_button.place(x=300, y=700, width=198, height=70)

        login_button = InterActiveButton(self, text="Login", command=self.window.show_page("LoginPage"), bg="#4a2175")
        login_button.place(x=501, y=700, width=197, height=70)

        exit_button = InterActiveButton(self, text="Exit", command=self.exit_event, bg="#752121")
        exit_button.place(x=701, y=700, width=199, height=70)

        # place username entry
        self.create_text(600, 280, text="Username", font=("Arial", 15, "bold"))
        self.username_entry.place(x=300, y=300, width=600, height=50)

        # place password entry
        self.create_text(600, 380, text="Password", font=("Arial", 15, "bold"))
        self.password_entry.place(x=300, y=400, width=600, height=50)

        # place email entry
        self.create_text(600, 480, text="Email", font=("Arial", 15, "bold"))
        self.email_entry.place(x=300, y=500, width=600, height=50)

    def lock_entries(self):
        """
        Lock the entries while used for signuping.
        """

        # lock the entries to prevent user from changing them
        self.username_entry.config(state="disabled")
        self.password_entry.config(state="disabled")
        self.email_entry.config(state="disabled")

        # lock the entries in the login page
        self.window.page_instances["LoginPage"].username_entry.config(state="disabled")
        self.window.page_instances["LoginPage"].password_entry.config(state="disabled")

    def unlock_entries(self):
        """
        Unlock the entries while used for signuping.
        """

        # unlock the entries to allow user to change them
        self.username_entry.config(state="enabled")
        self.password_entry.config(state="enabled")
        self.email_entry.config(state="enabled")

        # unlock the entries in the login page
        self.window.page_instances["LoginPage"].username_entry.config(state="enabled")
        self.window.page_instances["LoginPage"].password_entry.config(state="enabled")

    def submit_signup_info(self):
        """
        Submit the signup information to the server.
        """

        # lock the entries to prevent user from changing them
        self.lock_entries()

        # get the information from the entries
        username_to_submit: str = self.username.get()
        password_to_submit: str = self.password.get()
        email_to_submit: str = self.email.get()

        # check if the user is already logged in
        if not self.window.client.username is None:
            return

        # check if the data is valid
        try:
            cmd: Command = Command("SIGNUP", username_to_submit, password_to_submit, email_to_submit)
        except:
            self.update_message(
                "Please enter a valid username, password and email.\nThe username, password and email must not contain spaces.")
            self.unlock_entries()
            return

        try:
            # send the command to the server and get the response
            validity, response = self.window.client.send_and_get(cmd)
            if (not validity) or (response.command != CommandName.SUCCESS):
                raise Exception()
            else:
                self.window.client.username = username_to_submit
                if not self.get_user_score():
                    raise Exception()

                self.update_message("You have been signed up successfully.")

        except Exception as e:
            self.update_message(
                "Please try a different username, password and email.\nIf you have an account, please sign in.")
            self.unlock_entries()
