from __future__ import annotations
import tkinter as tk
from tkinter import ttk

from Client.Gui.Widgets.interactive_button import InterActiveButton
from Client.Gui.page_template import PageTemplate
from command import Command, CommandName


class GamePage(PageTemplate):
    """
    Game page of the application.
    """

    opponent_username: str | None = None
    letter: str | None = None

    def __init__(self, window: "Window"):
        """
        Initialize the game page.
        :param window: the window of the application.
        """
        super().__init__(window)

        # Timer variables
        self.timer_seconds: int = 0
        self.timer_minutes: int = 1
        self.timer_text: str = "%02d:%02d" % (self.timer_minutes, self.timer_seconds)
        self.timer_carry_on: bool = True
        self.timer_label: ttk.Label | None = None

        # entry variables
        self.country: tk.StringVar = tk.StringVar()
        self.city: tk.StringVar = tk.StringVar()
        self.animal: tk.StringVar = tk.StringVar()
        self.plant: tk.StringVar = tk.StringVar()
        self.boy: tk.StringVar = tk.StringVar()
        self.girl: tk.StringVar = tk.StringVar()

        self.country_entry: ttk.Entry = ttk.Entry(self, textvariable=self.country)
        self.city_entry: ttk.Entry = ttk.Entry(self, textvariable=self.city)
        self.animal_entry: ttk.Entry = ttk.Entry(self, textvariable=self.animal)
        self.plant_entry: ttk.Entry = ttk.Entry(self, textvariable=self.plant)
        self.boy_entry: ttk.Entry = ttk.Entry(self, textvariable=self.boy)
        self.girl_entry: ttk.Entry = ttk.Entry(self, textvariable=self.girl)

    def show_self(self) -> None:
        """
        Show the frame.
        """
        super().show_self()

        self.start_timer()
    
    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        # create page title
        self.create_text(600, 100, text=f"Your letter is {self.letter}!", font=("Arial", 60, "bold", "underline"))
        self.create_text(600, 170, text=f"Opponent: {self.opponent_username}", font=("Arial", 15, "bold"))

        self.timer_label = ttk.Label(self, text=self.timer_text)
        self.timer_label.place(x=800, y=400, width=50, height=50)

        # create the buttons
        submit_button = InterActiveButton(self, text="Submit", command=self.submit_answers)
        submit_button.place(x=300, y=600, width=600, height=100)

        exit_button = InterActiveButton(self, text="Exit", command=self.exit_event, bg="#752121")
        exit_button.place(x=990, y=720, width=200, height=70)


        # place country entry
        self.create_text(950, 262, text=":ארץ", font=("Arial", 15, "bold"))
        self.country_entry.place(x=300, y=250, width=600, height=30)

        # place city entry
        self.create_text(950, 312, text=":עיר", font=("Arial", 15, "bold"))
        self.city_entry.place(x=300, y=300, width=600, height=30)

        # place animal entry
        self.create_text(950, 362, text=":חי", font=("Arial", 15, "bold"))
        self.animal_entry.place(x=300, y=350, width=600, height=30)

        # place plant entry
        self.create_text(950, 412, text=":צומח", font=("Arial", 15, "bold"))
        self.plant_entry.place(x=300, y=400, width=600, height=30)

        # place boy entry
        self.create_text(950, 462, text=":ילד", font=("Arial", 15, "bold"))
        self.boy_entry.place(x=300, y=450, width=600, height=30)

        # place girl entry
        self.create_text(950, 512, text=":ילדה", font=("Arial", 15, "bold"))
        self.girl_entry.place(x=300, y=500, width=600, height=30)

    def lock_entries(self):
        """
        Lock the entries while used for submitting answers.
        """

        # lock the entries to prevent user from changing them
        self.country_entry.config(state="disabled")
        self.city_entry.config(state="disabled")
        self.animal_entry.config(state="disabled")
        self.plant_entry.config(state="disabled")
        self.boy_entry.config(state="disabled")
        self.girl_entry.config(state="disabled")

    def unlock_entries(self):
        """
        Unlock the entries while used for submitting answers.
        """

        # unlock the entries to allow user to change them
        self.country_entry.config(state="enabled")
        self.city_entry.config(state="enabled")
        self.animal_entry.config(state="enabled")
        self.plant_entry.config(state="enabled")
        self.boy_entry.config(state="enabled")
        self.girl_entry.config(state="enabled")

    def dec_timer(self) -> None:
        """
        Decrease the timer by 1 second.
        """

        self.timer_seconds -= 1

        if self.timer_seconds == -1:
            self.timer_seconds = 59
            self.timer_minutes -= 1

        if self.timer_minutes == -1:
            return

        # change timer display text
        self.timer_text = "%02d:%02d" % (self.timer_minutes, self.timer_seconds)
        self.timer_label.configure(text=self.timer_text)
        self.timer_label.update_idletasks()

        # schedule next update 1 second later
        self.window.after(1000, self.update)

    def start_timer(self) -> None:
        """
        Start the timer.
        """

        self.window.after(1000, self.update)


    def submit_answers(self):
        """
        Get the user score from the server and save it in the client.
        """

        # send the command to the server and get the response
        validity, response = self.window.client.send_and_get(Command(CommandName.INFO_REQUEST.value))
        if (not validity) or (response.command != CommandName.INFO_RESPONSE):
            # TODO
            return
        else:
            self.window.client.score = response.args
            self.window.page_instances["StartPage"].update_user()
            return