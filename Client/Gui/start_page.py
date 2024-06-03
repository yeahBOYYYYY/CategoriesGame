from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from Client.Gui.login_page import LoginPage
from Client.Gui.signup_page import SignupPage


class StartPage(ttk.Frame):
    def __init__(self, parent: tk.Canvas, controller: Window):
        """
        Initialize the start page of the application.
        :param parent: the parent of the frame.
        :param controller: the main window of the application.
        """
        super().__init__()

        # label of frame Layout 2
        label = ttk.Label(self, text="Startpage")

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=controller.show_login_page)

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=0, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=controller.show_signup_page)

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=0, padx=10, pady=10)
