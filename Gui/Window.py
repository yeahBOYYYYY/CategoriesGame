import tkinter as tk
from PIL import Image, ImageTk


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Categories game")

        # Load background image
        self.bg_image = Image.open("background_image.jpg")

        # Create canvas for background
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        # Create background image on canvas
        self.bg_photo = None
        self.bg_image_id = None
        self.resize_background(None)

        self.canvas.bind("<Configure>", self.resize_background)  # Bind the background image to resize event

        self.create_buttons()  # Add buttons

        self.root.mainloop()  # Start the main loop of tkinter

    def resize_background(self, event: tk.Event | None) -> None:
        """
        Resize the background image to fit the canvas size.
        :param event: the resize event.
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

    def create_buttons(self):
        # Create buttons
        self.top_button = tk.Button(self.root, text="Top Button", command=self.on_top_button_click)
        self.bottom_left_button = tk.Button(self.root, text="Bottom Left Button",
                                            command=self.on_bottom_left_button_click)
        self.bottom_right_button = tk.Button(self.root, text="Bottom Right Button",
                                             command=self.on_bottom_right_button_click)

        # Place buttons on the canvas
        self.top_button.place(relx=0.5, rely=0.1, anchor="center")
        self.bottom_left_button.place(relx=0.25, rely=0.9, anchor="center")
        self.bottom_right_button.place(relx=0.75, rely=0.9, anchor="center")

    def on_top_button_click(self):
        print("Top button clicked")

    def on_bottom_left_button_click(self):
        print("Bottom left button clicked")

    def on_bottom_right_button_click(self):
        print("Bottom right button clicked")

if __name__ == "__main__":
    Window()