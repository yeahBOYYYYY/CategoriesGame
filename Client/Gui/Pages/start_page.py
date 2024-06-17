from __future__ import annotations

import tkinter
from tkinter import ttk

from Client.Gui.Widgets.interactive_button import InterActiveButton
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

        # create the start button
        self.start_button = InterActiveButton(self, text="Start game", command=self.start_game_if_valid)

        # initialize the user text id
        self.user_txt = ttk.Label(self, text="", font = ("Arial", 20, "bold"))

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        # create the text
        # self.create_text(600, 100, text="!משחק ארץ עיר אחד על אחד", fill="#05fafa", font=("Arial", 60, "bold"))
        self.window.create_text_with_outline(self, 600, 100, "#05fafa", "black",
                                             text="!משחק ארץ עיר אחד על אחד",
                                             font=("Arial", 60, "bold")
        )

        # create the start button
        self.start_button.place(x=300, y=300, width=600, height=98)

        # create the buttons
        login_button = InterActiveButton(self, text="Login", command=self.window.show_page("LoginPage"), bg="#213c75")
        login_button.place(x=300, y=400, width=198, height=70)

        signup_button = InterActiveButton(self, text="Signup", command=self.window.show_page("SignupPage"), bg="#4a2175")
        signup_button.place(x=501, y=400, width=197, height=70)

        exit_button = InterActiveButton(self, text="Exit", command=self.exit_event, bg="#752121")
        exit_button.place(x=701, y=400, width=199, height=70)

        # self.user_txt.config(text=f"Username: {self.window.client.username}\n Wins: {self.window.client.score[0]}\n Losses: {self.window.client.score[1]}")
        # self.user_txt.place(x=600, y=600)

    def start_game_if_valid(self) -> None:
        """
        Start the game if the user is valid.
        """

        if self.window.client.username is None:
            self.window.show_page("LoginPage")()
        else:
            self.window.show_page("WaitingPage")()

    def update_user(self) -> None:
        """
        Update the user welcome text.
        """

        self.user_txt.config(text=f"Username: {self.window.client.username}\n Wins: {self.window.client.score[0]}\n Losses: {self.window.client.score[1]}", justify="center")
        self.user_txt.place(relx=0.5, y=600, anchor=tkinter.CENTER)
        self.update_idletasks()