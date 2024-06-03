import tkinter as tk
from PIL import Image, ImageTk

def on_resize(event):
    # resize the background image to the size of label
    image = bgimg.resize((event.width, event.height), Image.Resampling.LANCZOS)
    # update the image of the label
    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)

root = tk.Tk()
root.geometry('800x600')

bgimg = Image.open('background_image.jpg') # load the background image
l = tk.Label(root)
l.place(x=0, y=0, relwidth=1, relheight=1) # make label l to fit the parent window always
l.bind('<Configure>', on_resize) # on_resize will be executed whenever label l is resized

tk.Label(root, text='Some File').grid(row=0)
e1 = tk.Entry(root)
e1.grid(row=0, column=1)

root.mainloop()