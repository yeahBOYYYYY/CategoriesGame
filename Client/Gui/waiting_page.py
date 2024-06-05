from __future__ import annotations

from tkinter import ttk

from Client.Gui.page_template import PageTemplate


class WaitingPage(PageTemplate):
    """
    Waiting page of the application.
    """

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        start_button = ttk.Button(self, text="Start")
        start_button.place(x=400, y=200, width=50, height=50)
