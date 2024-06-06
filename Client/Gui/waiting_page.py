from __future__ import annotations

import threading
from tkinter import ttk

from Client.Gui.page_template import PageTemplate
from command import Command, CommandName
from internal_exception import InternalException


class WaitingPage(PageTemplate):
    """
    Waiting page of the application.
    """

    def show_self(self) -> None:
        """
        Show the frame.
        """
        super().show_self()

        self.ask_to_play()

    def process_response(self):
        validity, response = self.window.client.send_and_get(Command(CommandName.WAITING.value))
        if (not validity) or (response.command != CommandName.MATCH):
            raise InternalException("Failed to send or get command from the server.")
        else:
            opponent_username: str = response.args[0]
            letter: str = response.args[1]

            print(f"Matched with {opponent_username} and got letter {letter}.")

        # TODO close thread

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

        exit_button = ttk.Button(self, text="Exit", command=self.exit_event)
        exit_button.place(x=500, y=200, width=50, height=50)
