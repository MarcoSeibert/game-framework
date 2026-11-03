import tkinter as tk
from tkinter import ttk

from gameframework.gui.theme import TITLE_FONT


class BaseView(ttk.Frame):
    """Basis-View mit Menüleiste und Titel; Spiele erben davon und packen ihre Widgets darunter."""

    def __init__(self, parent: tk.Tk, title: str = "") -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = None

        menu_bar = tk.Menu(parent)
        menu = tk.Menu(menu_bar, tearoff=False)
        menu.add_command(label="Zurück zum Menü", command=self.return_to_menu)
        menu.add_command(label="Beenden", command=self.quit)
        menu_bar.add_cascade(label="Menü", menu=menu)
        parent.config(menu=menu_bar)

        if title:
            ttk.Label(self, text=title, font=TITLE_FONT).pack(pady=10)

    def set_controller(self, controller) -> None:
        self.controller = controller

    def return_to_menu(self) -> None:
        self.parent.destroy()
        from main import main

        main()

    def quit(self) -> None:
        self.parent.destroy()
