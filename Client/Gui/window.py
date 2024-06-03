import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from Client.Gui.start_page import StartPage
from Client.Gui.login_page import LoginPage
from Client.Gui.signup_page import SignupPage
from Client.Gui.waiting_page import WaitingPage
from Client.Gui.game_page import GamePage


class Window(tk.Tk):
    """
    The main window of the application.
    """

    background_image_path: str = "background_image.jpg"
    pages = [StartPage, LoginPage, SignupPage, WaitingPage, GamePage]

    def __init__(self):
        """
        Initialize the main window of the application.
        """
        super().__init__()

        # set title and window size
        self.title("Categories game")
        self.geometry("600x400")

        # Create background image on canvas
        self.bg_image: Image = Image.open(self.background_image_path)
        self.PhotoImage = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas for the pages
        self.canvas: tk.Canvas | None = None
        self.initialize_canvas()

        # pages in the application
        self.page_instances: dict[ttk.Frame] = {}
        self.initialize_pages()

        # Start the main loop of tkinter
        self.mainloop()

    def initialize_image(self) -> None:
        """
        Initialize the background image.
        """

        # place the image in the canvas behind everything
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the background image to resize event
        self.image_label.bind("<Configure>", self.resize_background)

    def initialize_canvas(self) -> None:
        """
        Initialize the canvas of the pages.
        """

        self.canvas = tk.Canvas(self)

        self.canvas.create_image(0, 0, image=self.PhotoImage, anchor="nw")

        # make the canvas fit the parent window always and have a grid layout
        self.canvas.grid(sticky='nsew')
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

    def initialize_pages(self) -> None:
        """
        Initialize the pages of the application.
        """

        for P in self.pages:
            page = P(self.canvas, self)  # create instance of the page
            self.page_instances[P] = page
            page.grid(row=0, column=0, sticky="nsew")

        # show the start page
        self.show_page(StartPage)

    def resize_background(self, event: tk.Event | None) -> None:
        """
        Resize the background image to fit the canvas size.
        """

        # resize the background image to the size of label
        image = self.bg_image.resize((event.width, event.height), Image.Resampling.LANCZOS)
        # update the image of the label
        self.image_label.image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image_label.image)

    def show_page(self, cont: ttk.Frame) -> None:
        """
        Show the page with the given key.
        :param cont: the key of the page to show.
        """

        page = self.page_instances[cont]
        page.tkraise()  # display the page


    def show_start_page(self) -> None:
        """
        Show the start page.
        """

        self.show_page(StartPage)

    def show_login_page(self) -> None:
        """
        Show the start page.
        """

        self.show_page(LoginPage)

    def show_signup_page(self) -> None:
        """
        Show the start page.
        """

        self.show_page(SignupPage)

    def show_waiting_page(self) -> None:
        """
        Show the waiting page.
        """

        self.show_page(WaitingPage)

    def show_game_page(self) -> None:
        """
        Show the game page.
        """

        self.show_page(GamePage)


if __name__ == "__main__":
    Window()
