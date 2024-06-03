from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class GamePage(ttk.Frame):
    def __init__(self, parent: tk.Canvas, controller: Window):
        """
        Initialize the game page of the application.
        :param parent: the parent of the frame.
        :param controller: the main window of the application.
        """
        super().__init__()
