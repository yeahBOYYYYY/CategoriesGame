import tkinter as tk
from PIL import Image, ImageTk


class MovingBackgroundApp:
    def __init__(self, root):
        self.root = root

        # Set the window title in RTL format
        self.set_rtl_title("عنوان يمين لليسار")

        # Load background image
        self.bg_image = Image.open("background_image.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create canvas for background
        self.canvas = tk.Canvas(self.root, width=self.bg_photo.width(), height=self.bg_photo.height())
        self.canvas.pack(fill="both", expand=True)

        # Create background image on canvas
        self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Add buttons
        self.create_buttons()

        # Initialize background movement
        self.bg_x = 0
        self.bg_y = 0
        self.move_speed = 2  # Speed of the background movement

        # Start moving background
        self.move_background()

    def set_rtl_title(self, title):
        rtl_title = title[::-1]  # Reverse the title text
        self.root.title(rtl_title)

    def create_buttons(self):
        # Create buttons
        self.top_button = tk.Button(self.root, text="Top Button", command=self.on_top_button_click)
        self.bottom_left_button = tk.Button(self.root, text="Bottom Left Button",
                                            command=self.on_bottom_left_button_click)
        self.bottom_right_button = tk.Button(self.root, text="Bottom Right Button",
                                             command=self.on_bottom_right_button_click)

        # Place buttons on the canvas
        self.canvas.create_window(150, 50, window=self.top_button, anchor="nw")
        self.canvas.create_window(50, 400, window=self.bottom_left_button, anchor="nw")
        self.canvas.create_window(250, 400, window=self.bottom_right_button, anchor="nw")

    def on_top_button_click(self):
        print("Top button clicked")

    def on_bottom_left_button_click(self):
        print("Bottom left button clicked")

    def on_bottom_right_button_click(self):
        print("Bottom right button clicked")

    def move_background(self):
        # Move the background image
        self.bg_x -= self.move_speed
        if self.bg_x <= -self.bg_photo.width():
            self.bg_x = 0

        self.canvas.coords(self.bg_image_id, self.bg_x, self.bg_y)
        self.canvas.create_image(self.bg_x + self.bg_photo.width(), self.bg_y, image=self.bg_photo, anchor="nw")

        # Repeat the movement
        self.root.after(50, self.move_background)


# Create the main window
root = tk.Tk()
app = MovingBackgroundApp(root)
root.mainloop()
