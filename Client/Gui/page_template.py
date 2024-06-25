from __future__ import annotations

import tkinter
import tkinter as tk
from tkinter import ttk

from command import Command, CommandName


class PageTemplate(tk.Canvas):
    """
    Template to create a new page in the application.
    """

    def __init__(self, window: "Window"):
        """
        Template to create a new page in the application.
        :param window: the window parent of the frame.
        """
        super().__init__(window, width=window.window_size[0], height=window.window_size[1])

        self.window: "Window" = window

        error_style = ttk.Style()
        error_style.configure("Error.TLabel", foreground="red", background="white")
        self.error_text = ttk.Label(self, text="", font=("Arial", 20, "bold"), style="Error.TLabel")

    def show_self(self) -> None:
        """
        Show the frame.
        """

        # Load the background image and resize the image to fit the window
        self.create_image(0, 0, image=self.window.image, anchor="nw")

        self.place_widgets()

        self.pack(fill="both", expand=True)

    def unshow_self(self):
        """
        Unshow the frame.
        """

        self.pack_forget()

    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        pass

    def exit_event(self):
        """
        If got here, then the client wishes to close the game.
        """

        self.window.destroy()

    def get_user_score(self) -> bool:
        """
        Get the user score from the server and save it in the client.
        :returns: True if the user score was successfully retrieved, False otherwise.
        """

        try:
            # send the command to the server and get the response
            validity, response = self.window.client.send_and_get(Command(CommandName.INFO_REQUEST.value))
            if (not validity) or (response.command != CommandName.INFO_RESPONSE):
                return False
            else:
                self.window.client.score = response.args
                self.window.page_instances["StartPage"].update_user()
                return True
        except:
            return False

    def update_message(self, text: str, y: int = 200) -> None:
        """
        Update the main message.
        :param text: the text to update.
        :param y: the y position to place the text at.
        """

        self.error_text.config(text=text, justify="center")
        self.error_text.place(relx=0.5, y=y, anchor=tkinter.CENTER)
        self.update_idletasks()