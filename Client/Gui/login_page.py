from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from Client.Gui.page_template import PageTemplate
from command import Command, CommandName


class LoginPage(PageTemplate):
    """
    Login page of the application.
    """

    def __init__(self, window: "Window") -> None:
        """
        Initialize the login page.
        :param window: The window of the application.
        """
        super().__init__(window)

        self.username: tk.StringVar = tk.StringVar()
        self.password: tk.StringVar = tk.StringVar()

        self.username_entry: ttk.Entry = ttk.Entry(self, textvariable=self.username)
        self.password_entry: ttk.Entry = ttk.Entry(self, textvariable=self.password)

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        start_button = ttk.Button(self, text="Back", command=self.window.show_page("StartPage"))
        start_button.place(x=800, y=200, width=50, height=50)

        login_button = ttk.Button(self, text="Signup", command=self.window.show_page("SignupPage"))
        login_button.place(x=300, y=200, width=50, height=50)

        signup_button = ttk.Button(self, text="Submit", command=self.submit_login_info)
        signup_button.place(x=400, y=200, width=50, height=50)

        exit_button = ttk.Button(self, text="Exit", command=self.exit_event)
        exit_button.place(x=500, y=200, width=50, height=50)

        # place entries
        self.username_entry.place(x=400, y=300, width=200, height=50)
        self.password_entry.place(x=400, y=400, width=200, height=50)

    def lock_entries(self):
        """
        Lock the entries while used for logging.
        """

        # lock the entries to prevent user from changing them
        self.username_entry.config(state="disabled")
        self.password_entry.config(state="disabled")

        # lock the entries in the signup page
        self.window.page_instances["SignupPage"].username_entry.config(state="disabled")
        self.window.page_instances["SignupPage"].password_entry.config(state="disabled")
        self.window.page_instances["SignupPage"].email_entry.config(state="disabled")

    def unlock_entries(self):
        """
        Unlock the entries while used for logging.
        """

        # unlock the entries to allow user to change them
        self.username_entry.config(state="enabled")
        self.password_entry.config(state="enabled")

        # unlock the entries in the signup page
        self.window.page_instances["SignupPage"].username_entry.config(state="enabled")
        self.window.page_instances["SignupPage"].password_entry.config(state="enabled")
        self.window.page_instances["SignupPage"].email_entry.config(state="enabled")

    def submit_login_info(self):
        """
        Submit the login information to the server.
        :return:
        """

        # lock the entries to prevent user from changing them
        self.lock_entries()

        # get the information from the entries
        username_to_submit: str = self.username.get()
        password_to_submit: str = self.password.get()

        # check if the user is already logged in
        if not self.window.client.username is None:
            # TODO
            return

        # check if the data is valid
        try:
            cmd: Command = Command("LOGIN", username_to_submit, password_to_submit)
        except:
            # TODO
            self.unlock_entries()
            return

        # send the command to the server and get the response
        validity, response = self.window.client.send_and_get(cmd)
        if (not validity) or (response.command != CommandName.SUCCESS):
            # TODO
            self.unlock_entries()
            return
        else:
            self.window.client.username = username_to_submit
            return
