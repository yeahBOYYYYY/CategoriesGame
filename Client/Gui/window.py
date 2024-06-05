import tkinter as tk

from PIL import Image, ImageTk

from Client.Gui.game_page import GamePage
from Client.Gui.login_page import LoginPage
from Client.Gui.page_template import PageTemplate
from Client.Gui.signup_page import SignupPage
from Client.Gui.start_page import StartPage
from Client.Gui.waiting_page import WaitingPage
from internal_exception import InternalException


class Window(tk.Tk):
    """
    The main window of the application.
    """

    window_size: tuple[int, int] = (1200, 800)
    background_image_path: str = "background_image.jpg"
    pages = [StartPage, LoginPage, SignupPage, WaitingPage, GamePage, PageTemplate]

    def __init__(self):
        """
        Initialize the main window of the application.
        """
        super().__init__()

        # set title and window size
        self.title("Categories game")
        self.geometry(f"{self.window_size[0]}x{self.window_size[1]}")
        self.resizable(False, False)

        self.image = self.initialize_image()

        # pages in the application
        self.page_instances: dict[str, PageTemplate] = {}
        self.initialize_pages()

        # Start the main loop of tkinter
        self.mainloop()

    def initialize_image(self) -> ImageTk.PhotoImage:
        bg_image_raw = Image.open(self.background_image_path)
        bg_image_resized = bg_image_raw.resize(self.window_size, Image.Resampling.LANCZOS)
        bg_image: ImageTk.PhotoImage = ImageTk.PhotoImage(bg_image_resized)
        return bg_image

    def show_page(self, page_name: str) -> None:
        """
        Show the page with the given name.
        :param page_name: the page name of the page to show.
        """

        if page_name not in self.page_instances:
            raise InternalException(f"Page {page_name} not found.")

        page = self.page_instances[page_name]
        tk.Misc.lift(page)  # display the page

    def initialize_pages(self) -> None:
        """
        Initialize the pages of the application.
        """

        for P in self.pages:
            page = P(self)  # create instance of the page
            self.page_instances[P.__name__] = page

        # show the start page
        self.show_page("PageTemplate")


if __name__ == "__main__":
    Window()
