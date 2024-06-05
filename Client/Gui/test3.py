import tkinter as tk

from PIL import Image, ImageTk

root = tk.Tk()
root.title("Form with Background Image")
root.geometry("800x600")

root.resizable(False, False)

# Resize the image to fit the window
bg_image = Image.open("background_image.jpg").resize((800, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas and add the background image
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

start_button = tk.Button(root, text="Start", width=20, height=2)
sign_in_button = tk.Button(root, text="Sign-in", width=20, height=2)
sign_up_button = tk.Button(root, text="Sign-up", width=20, height=2)

# Add buttons to canvas
canvas.create_window(400, 200, window=start_button)
canvas.create_window(300, 250, window=sign_in_button)
canvas.create_window(500, 250, window=sign_up_button)

root.mainloop()
