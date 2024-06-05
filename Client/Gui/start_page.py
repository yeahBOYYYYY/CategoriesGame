from __future__ import annotations

from tkinter import ttk

from Client.Gui.page_template import PageTemplate


class StartPage(PageTemplate):
    """
    Start page of the application.
    """

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        start_button = ttk.Button(self, text="Start game")
        start_button.place(x=800, y=200, width=50, height=50)

        start_button = ttk.Button(self, text="Login")
        start_button.place(x=300, y=200, width=50, height=50)

        start_button = ttk.Button(self, text="Signup")
        start_button.place(x=400, y=200, width=50, height=50)

        start_button = ttk.Button(self, text="Exit")
        start_button.place(x=500, y=200, width=50, height=50)
