from __future__ import annotations

from tkinter import ttk

from Client.Gui.page_template import PageTemplate


class SignupPage(PageTemplate):
    """
    Signup page of the application.
    """

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        start_button = ttk.Button(self, text="SIGNUP")
        start_button.place(x=400, y=200, width=50, height=50)
