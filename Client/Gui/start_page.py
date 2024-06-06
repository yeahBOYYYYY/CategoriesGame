from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from Client.Gui.page_template import PageTemplate


class StartPage(PageTemplate):
    """
    Start page of the application.
    """

    def __init__(self, window: "Window") -> None:
        """
        Initialize the login page.
        :param window: The window of the application.
        """
        super().__init__(window)

        self.start_button = ttk.Button(self, text="Start game", state="disabled", command=self.window.show_page("WaitingPage"))

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        self.start_button.place(x=800, y=200, width=50, height=50)

        login_button = ttk.Button(self, text="Login", command=self.window.show_page("LoginPage"))
        login_button.place(x=300, y=200, width=50, height=50)

        signup_button = ttk.Button(self, text="Signup", command=self.window.show_page("SignupPage"))
        signup_button.place(x=400, y=200, width=50, height=50)

        exit_button = ttk.Button(self, text="Exit", command=self.exit_event)
        exit_button.place(x=500, y=200, width=50, height=50)
