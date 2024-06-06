from __future__ import annotations

from tkinter import ttk

from Client.Gui.page_template import PageTemplate


class GamePage(PageTemplate):
    """
    Game page of the application.
    """

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        start_button = ttk.Button(self, text="Back", command=self.window.show_page("StartPage"))
        start_button.place(x=800, y=200, width=50, height=50)

        login_button = ttk.Button(self, text="Login", command=self.window.show_page("LoginPage"))
        login_button.place(x=300, y=200, width=50, height=50)

        signup_button = ttk.Button(self, text="Resign")
        signup_button.place(x=400, y=200, width=50, height=50)

        exit_button = ttk.Button(self, text="Exit", command=self.exit_event)
        exit_button.place(x=500, y=200, width=50, height=50)
