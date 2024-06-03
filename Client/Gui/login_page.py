from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class LoginPage(ttk.Frame):
    def __init__(self, parent: tk.Canvas, controller: Window):
        """
        Initialize the login page of the application.
        :param parent: the parent of the frame.
        :param controller: the main window of the application.
        """
        super().__init__()

        label = ttk.Label(self, text="Login page")

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_start_page)

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_signup_page)

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)