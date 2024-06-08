from __future__ import annotations

from tkinter import ttk

from Client.Gui.page_template import PageTemplate


class GamePage(PageTemplate):
    """
    Game page of the application.
    """

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

        self.timer_label = ttk.Label(self, text=self.timer_text)
        self.timer_label.place(x=800, y=400, width=50, height=50)

        start_button = ttk.Button(self, text="Back", command=self.window.show_page("StartPage"))
        start_button.place(x=800, y=200, width=50, height=50)

        login_button = ttk.Button(self, text="Login", command=self.window.show_page("LoginPage"))
        login_button.place(x=300, y=200, width=50, height=50)

        signup_button = ttk.Button(self, text="Resign")
        signup_button.place(x=400, y=200, width=50, height=50)

        exit_button = ttk.Button(self, text="Exit", command=self.exit_event)
        exit_button.place(x=500, y=200, width=50, height=50)

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
        self.timer_text = "%02d:%02d" % (self.timer_seconds, self.timer_seconds)
        self.timer_label.configure(text=self.timer_text)

        # schedule next update 1 second later
        self.window.after(1000, self.update)

    def start_timer(self) -> None:
        """
        Start the timer.
        """

        self.window.after(1000, self.update)
