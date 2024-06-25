import tkinter as tk


class InterActiveButton(tk.Button):
    """
    This button expands when the user hovers over it and shrinks when
    the cursor leaves the button.

    If you want the button to expand in both directions, just use:
        button = InterActiveButton(root, text="Button", width=200, height=50)
        button.pack()
    If you want the button to only expand to the right use:
        button = InterActiveButton(root, text="Button", width=200, height=50)
        button.pack(anchor="w")

    This button should work with all geometry managers.

    This button is based on the answer from here: https://stackoverflow.com/questions/68166640/interactive-and-nice-looking-buttons-in-tkinter
    """

    def __init__(self, master, max_expansion: int = 12, bg="#5ab35b",
                 fg="white", **kwargs):
        """
        Constructor for the InterActiveButton class.
        :param master: The parent widget.
        :param max_expansion: The maximum width the button can expand to.
        :param bg: The background color of the button.
        :param fg: The foreground color of the button.
        :param kwargs: The keyword arguments to pass to the Button class.
        """

        # Save some variables for later:
        self.max_expansion = max_expansion
        self.bg = bg
        self.fg = fg

        # To use the button's width in pixels:
        # From here: https://stackoverflow.com/a/46286221/11106801
        self.pixel = tk.PhotoImage(width=1, height=1)

        # The default button arguments:
        button_args = dict(cursor="hand2", bd=0, font=("arial", 18, "bold"),
                           height=50, compound="c", activebackground=bg,
                           image=self.pixel, activeforeground=fg)
        button_args.update(kwargs)
        super().__init__(master, bg=bg, fg=fg, **button_args)

        # Bind to the cursor entering and exiting the button:
        super().bind("<Enter>", self.on_hover)
        super().bind("<Leave>", self.on_leave)

        # Save some variables for later:
        self.base_width = button_args.pop("width", 200)
        self.width = self.base_width
        # `self.mode` can be "increasing"/"decreasing"/None only
        # It stops a bug where if the user quickly hovers over
        # the button doesn't go back to normal
        self.mode = None

    def increase_width(self) -> None:
        """
        This function increases the width of the button.
        """

        if self.width <= self.base_width + self.max_expansion:
            if self.mode == "increasing":
                self.width += 1
                super().config(width=self.width)
                super().after(5, self.increase_width)

    def decrease_width(self) -> None:
        """
        This function decreases the width of the button.
        """

        if self.width > self.base_width:
            if self.mode == "decreasing":
                self.width -= 1
                super().config(width=self.width)
                super().after(5, self.decrease_width)

    def on_hover(self, event: tk.Event = None) -> None:
        """
        This function is called when the cursor enters the button.
        :param event: The event object.
        """

        # Improvement: use integers instead of "increasing" and "decreasing"
        self.mode = "increasing"
        # Swap the `bg` and the `fg` of the button
        super().config(bg=self.fg, fg=self.bg)
        super().after(5, self.increase_width)

    def on_leave(self, event: tk.Event = None) -> None:
        """
        This function is called when the cursor leaves the button.
        :param event: The event object.
        """

        # Improvement: use integers instead of "increasing" and "decreasing"
        self.mode = "decreasing"
        # Reset the `fg` and `bg` of the button
        super().config(bg=self.bg, fg=self.fg)
        super().after(5, self.decrease_width)
