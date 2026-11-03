import tkinter as tk
from tkinter import ttk

from gameframework.gui.theme import TITLE_FONT, configure_styles
from gameframework.registry import get_game, registered_games


class GameApp(tk.Tk):
    """Vollbild-Fenster, das Model, View und Controller eines registrierten Spiels verdrahtet."""

    def __init__(self, game_name: str, options: dict = None) -> None:
        super().__init__()
        configure_styles()
        self.definition = get_game(game_name)
        self.title(self.definition.name)
        self.options = options if options else {}
        self.attributes("-fullscreen", True)

        self.model = self.definition.model_class(self.options)
        self.view = self.definition.view_class(self)
        self.view.pack(fill="both", expand=True)
        self.controller = self.definition.controller_class(self.model, self.view)
        self.view.set_controller(self.controller)
        self.model.start()


class StartApp(tk.Tk):
    """Startmenü: listet alle registrierten Spiele auf und startet das ausgewählte."""

    def __init__(self) -> None:
        super().__init__()
        configure_styles()
        self.title("Game Framework")
        self.geometry("520x320")
        self.resizable(False, False)

        ttk.Label(self, text="Spiel auswählen", font=TITLE_FONT).pack(pady=10)
        games = registered_games()
        self.chosen_game = tk.StringVar(value=next(iter(games), ""))
        for name, definition in games.items():
            text = f"{name} – {definition.description}" if definition.description else name
            ttk.Radiobutton(
                self,
                text=text,
                variable=self.chosen_game,
                value=name,
                style="Basic.TRadiobutton",
            ).pack(anchor="w", padx=40)
        ttk.Button(
            self,
            text="Spielen!",
            style="Basic.TButton",
            command=self.start_selected,
        ).pack(pady=10)
        ttk.Button(
            self, text="Beenden", style="Basic.TButton", command=self.destroy
        ).pack()

    def start_selected(self) -> None:
        name = self.chosen_game.get()
        if not name:
            return
        self.destroy()
        app = GameApp(name)
        app.mainloop()
