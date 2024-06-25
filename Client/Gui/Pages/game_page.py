from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from Client.Gui.Widgets.interactive_button import InterActiveButton
from Client.Gui.page_template import PageTemplate
from command import Command, CommandName


class GamePage(PageTemplate):
    """
    Game page of the application.
    """

    heb_to_eng: dict[str, str] = {"א": "a", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "v", "ז": "z", "ח": "h",
                                  "ט": "t", "י": "y", "כ": "k", "ל": "l", "מ": "m", "נ": "n", "ס": "s", "ע": "a",
                                  "פ": "p", "צ": "c", "ק": "k", "ר": "r", "ש": "s", "ת": "t"
    }

    opponent_username: str | None = None
    letter: str | None = None
    threads: list[threading.Thread] = []  # list of threads to stop when the game ends
    game_result: int | None = None  # 0 for lose, 1 for win, -1 for error

    def __init__(self, window: "Window"):
        """
        Initialize the game page.
        :param window: the window of the application.
        """
        super().__init__(window)

        # the score of the user in this match
        self.evaluated_score: int = 0

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
    
    def place_widgets(self) -> None:
        """
        Place the widgets in the frame.
        """

        # create page title
        self.create_text(600, 100, text=f"Your letter is {self.letter}!", font=("Arial", 60, "bold", "underline"))
        self.create_text(600, 170, text=f"Opponent: {self.opponent_username}", font=("Arial", 15, "bold"))

        # create the buttons
        submit_button = InterActiveButton(self, text="Submit", command=self.evaluate_score)
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

    def exit_event(self):
        """
        If got here, then the client wishes to close the game.
        """

        for t in self.threads:  # stop all threads
            t.join()

        self.window.destroy()

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

    @staticmethod
    def camel_case(string: str) -> str:
        """
        Convert the string to camel case.
        :param string: the string to convert.
        :return: the string in camel case.
        """

        res = ""
        for word in string.split(" "):
            res += word.capitalize()
            res += " "
        return res.strip()

    def score_adder(self, answer: str, file_path: str) -> int:
        """
        Return how much to add to the score based on the answer, answer in Hebrew.
        :param answer: the answer to check.
        :param file_path: the path of the file to check the answer in.
        :return: the score of the answer.
        """

        if answer == "":
            return 0

        if answer[0] != self.letter:  # the first letter is not correct
            return 0

        with open(file_path, 'r', encoding="utf-8") as file:  # check in dataset
            for line in file:
                if answer in line:
                    return 2

        return 0  # answer not found

    def eng_score_adder(self, answer: str, file_path: str) -> int:
        """
        Return how much to add to the score based on the answer, answer in English.
        :param answer: the answer to check.
        :param file_path: the path of the file to check the answer in.
        :return: the score of the answer.
        """

        if answer == "":
            return 0

        if answer[0].lower() != self.heb_to_eng[self.letter]:  # the first letter is not correct
            return 0

        with open(file_path, 'r', encoding="utf-8") as file:  # check in dataset
            for line in file:
                if self.camel_case(answer) in line:
                    return 1

        return 0  # answer not found

    def evaluate_score(self) -> None:
        """
        Evaluate the score of the user and save it in self.evaluated_score.
        """

        # get the answers from the user
        country = self.country.get()
        city = self.city.get()
        animal = self.animal.get()
        plant = self.plant.get()
        boy = self.boy.get()
        girl = self.girl.get()

        tmp_score = 0  # initialize new score
        tmp_score += self.score_adder(country, "./Client/Answers/Country")
        tmp_score += self.score_adder(city, "./Client/Answers/CityHeb")
        tmp_score += self.eng_score_adder(city, "./Client/Answers/City")
        tmp_score += self.score_adder(animal, "./Client/Answers/Animal")
        tmp_score += self.score_adder(plant, "./Client/Answers/Plant")

        self.evaluated_score = tmp_score
        print(self.evaluated_score)
        # tmp_score += self.score_adder(boy, "./Client/Answers/Country")
        # tmp_score += self.score_adder(girl, "")

    def submit_answers(self) -> None:
        """
        Send the user score to the server and wait to get a response if you won.
        """

        self.lock_entries()

        # send the command to the server and get the response
        validity, response = self.window.client.send_and_get(
            Command(CommandName.ANSWERS.value, str(self.evaluated_score)))
        if (not validity) or (response.command.value not in [CommandName.SUCCESS.value, CommandName.FAIL.value]):
            # if the command is not valid set to error mode
            self.game_result = -1
            return
        elif response.command.value == CommandName.SUCCESS.value:
            # if the command is success set to win mode
            self.game_result = 1
        else:
            # if the command is fail set to lose mode
            self.game_result = 0

        # get the user score and update in StartPage
        self.get_user_score()


    def game_timer(self, duration: int = 60) -> None:
        """
        Start the game timer in a different thread.
        """

        # start a timer for the game
        t = threading.Timer(duration, self.submit_answers)
        t.start()
        self.threads.append(t)

        self.check_if_game_finished()

    def check_if_game_finished(self) -> None:
        """
        Check if the game has finished from tkinter main thread periodically.
        """

        if self.game_result is None:
            self.after(ms=1000, func=self.check_if_game_finished)
        else:
            self.window.show_page("StartPage")()
            self.window.page_instances["GamePage"] = GamePage(self.window)