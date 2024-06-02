import tkinter as tk

from PIL import Image, ImageTk

from start_page import StartPage
from login_page import LoginPage
from signup_page import SignupPage
from waiting_page import WaitingPage
from game_page import GamePage


class Window(tk.Tk):
    def __init__(self):
        """
        Initialize the main window of the application.
        """
        super().__init__()

        self.title("Categories game")

        # Load background image
        self.bg_image: Image = Image.open("background_image.jpg")

        # Create canvas for background
        self.canvas: tk.Canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Create background image on canvas
        self.bg_photo = None
        self.bg_image_id = None
        self.resize_background(None)
        self.canvas.bind("<Configure>", self.resize_background)  # Bind the background image to resize event

        # pages in the application
        self.pages: dict[tk.Frame] = {}

        # Initialize the pages
        for P in (StartPage, LoginPage, SignupPage, WaitingPage, GamePage):
            self.pages[P] = P(self.canvas, self)

        # show the start page
        self.show_page(StartPage)

        self.mainloop()  # Start the main loop of tkinter

    def resize_background(self, event: tk.Event | None) -> None:
        """
        Resize the background image to fit the canvas size.
        """

        # Get the new size of the canvas
        new_width = self.canvas.winfo_width()
        new_height = self.canvas.winfo_height()

        # Resize the background image
        resized_image = self.bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)

        # Delete the old image and create a new one
        if self.bg_image_id is not None:
            self.canvas.delete(self.bg_image_id)
        self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def show_page(self, cont) -> None:
        """
        Show the page with the given key.
        :param cont: the key of the page to show.
        """

        page = self.pages[cont]
        page.tkraise()  # display the page


if __name__ == "__main__":
    Window()
