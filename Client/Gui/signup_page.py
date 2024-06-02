import tkinter as tk
from tkinter import ttk


class SignupPage(tk.Frame):
    def __init__(self, parent: tk.Canvas, controller: tk.Tk):
        """
        Initialize the signup page of the application.
        :param parent: the parent of the frame.
        :param controller: the main window of the application.
        """

        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Signup page")

        # button1 = ttk.Button(self, text="Page 1",
        #                      command=lambda: controller.show_frame(Page1))

        # # putting the button in its place by
        # # using grid
        # button1.grid(row=1, column=1, padx=10, pady=10)
        #
        # ## button to show frame 2 with text layout2
        # button2 = ttk.Button(self, text="Page 2",
        #                      command=lambda: controller.show_frame(Page2))
        #
        # # putting the button in its place by
        # # using grid
        # button2.grid(row=2, column=1, padx=10, pady=10)