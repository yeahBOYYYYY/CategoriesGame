import tkinter as tk
from typing import Callable

from PIL import Image, ImageTk

from Client.Gui.Pages.game_page import GamePage
from Client.Gui.Pages.login_page import LoginPage
from Client.Gui.Pages.signup_page import SignupPage
from Client.Gui.Pages.start_page import StartPage
from Client.Gui.Pages.waiting_page import WaitingPage
from Client.Gui.page_template import PageTemplate
from internal_exception import InternalException


class Window(tk.Tk):
    """
    The main window of the application.
    """

    window_size: tuple[int, int] = (1200, 800)
    pages = [StartPage, LoginPage, SignupPage, WaitingPage, GamePage]

    showing_page: str | None = None

    def __init__(self, client: "Client", background_image_path: str = "./Client/Gui/background_image.jpg"):
        """
        Initialize the main window of the application.
        :param client: The client of the application.
        :param background_image_path: The path to the background image of the window.
        """
        super().__init__()

        self.client: "Client" = client
        self.background_image_path: str = background_image_path

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
        """
        Initialize the background image of the window.
        :return: the background image of the window.
        """

        bg_image_raw = Image.open(self.background_image_path)
        bg_image_resized = bg_image_raw.resize(self.window_size, Image.Resampling.LANCZOS)
        bg_image: ImageTk.PhotoImage = ImageTk.PhotoImage(bg_image_resized)
        return bg_image

    def show_page(self, page_name: str) -> Callable[[], None]:
        """
        Show the page with the given name.
        :param page_name: the page name of the page to show.
        :return: the function to show the page, to give button command to call.
        """

        def inner_show_page() -> None:
            """
            Show the page with the given name.
            """

            # page not found
            if page_name not in self.page_instances:
                raise InternalException(f"Page {page_name} not found.")

            page = self.page_instances[page_name]

            # hide the current page
            if (self.showing_page != page_name) and (not self.showing_page is None):
                self.page_instances[self.showing_page].unshow_self()

            # show the new page
            page.show_self()
            self.showing_page = page_name

        return inner_show_page

    def initialize_pages(self) -> None:
        """
        Initialize the pages of the application.
        """

        for P in self.pages:
            page = P(self)  # create instance of the page
            self.page_instances[P.__name__] = page

        # show the start page
        self.show_page("StartPage")()

    @staticmethod
    def create_text_with_outline(canvas: tk.Canvas, x: int, y: int, text_color: str, outline_color: str,
                                 **kwargs) -> None:
        """
        Create text with an outline.
        :param canvas: The canvas to draw the text on.
        :param x: The x coordinate of the text.
        :param y: The y coordinate of the text.
        :param text_color: The color of the text.
        :param outline_color: The color of the outline.
        :param kwargs: The other arguments to pass to the create_text function.
        """

        # Create the outline text
        canvas.create_text(x, y, fill=outline_color, **kwargs)

        # Create the actual text slightly offset from the outline
        canvas.create_text(x - 1, y - 1, fill=text_color, **kwargs)


if __name__ == "__main__":
    Window(None, "background_image.jpg")
