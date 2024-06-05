import tkinter as tk

from PIL import Image, ImageTk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load the background image and resize it to the desired size
        bg_image = Image.open("background_image.jpg")
        bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a canvas and add the background image
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Create a frame and place it on top of the canvas
        self.frame = tk.Frame(self.canvas, bg="white")
        self.frame.place(relwidth=1, relheight=1)

        # Add a button to the frame
        self.button = tk.Button(self.frame, text="Click me!")
        self.button.pack(pady=20)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
