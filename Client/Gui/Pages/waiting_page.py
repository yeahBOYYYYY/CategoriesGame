from __future__ import annotations

import threading
from tkinter import ttk

from Client.Gui.Widgets.interactive_button import InterActiveButton
from Client.Gui.page_template import PageTemplate
from command import Command, CommandName
from internal_exception import InternalException


class WaitingPage(PageTemplate):
    """
    Waiting page of the application.
    """

    def __init__(self, window: "Window"):
        """
        Initialize the waiting page.
        :param window: the main window of the application.
        """
        super().__init__(window)
        self.letter: str | None = None
        self.opponent_username: str | None = None

    def show_self(self) -> None:
        """
        Show the frame.
        """
        super().show_self()

        self.ask_to_play()

    def process_response(self):
        """
        Process the response from the server.
        """

        validity, response = self.window.client.send_and_get(Command(CommandName.WAITING.value))
        if (not validity) or (response.command != CommandName.MATCH):
            raise InternalException("Failed to send or get command from the server.")
        else:
            self.opponent_username = response.args[0]
            self.letter = response.args[1]

            print(f"Matched with {self.opponent_username} and got letter {self.letter}.")
            self.window.show_page("GamePage")()

    def ask_to_play(self) -> None:
        """
        Ask the server to play.
        """

        try:
            # send the command to the server and get the response
            t = threading.Thread(target=self.process_response)
            t.start()
        except Exception as e:
            print(e)

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        # create page title
        self.create_text(600, 200, text="Waiting for another player...", font=("Arial", 60, "bold"))

        # create the buttons
        exit_button = InterActiveButton(self, text="Exit", command=self.exit_event, bg="#752121")
        exit_button.place(x=300, y=600, width=600, height=98)
