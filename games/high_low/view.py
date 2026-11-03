import tkinter as tk
from tkinter import ttk

from gameframework.core.cards import Card
from gameframework.gui.base_view import BaseView
from gameframework.gui.card_view import card_text
from gameframework.gui.theme import BASIC_FONT, CARD_FONT, TITLE_FONT


class HighLowView(BaseView):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent, title="High / Low")

        self.card_label = ttk.Label(
            self, text="", font=CARD_FONT, relief="solid", width=18, padding=20
        )
        self.card_label.pack(pady=10)

        self.status_label = ttk.Label(self, text="", font=BASIC_FONT)
        self.status_label.pack(pady=5)

        self.score_label = ttk.Label(self, text="Punkte: 0", font=BASIC_FONT)
        self.score_label.pack(pady=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(
            button_frame, text="Höher", style="Basic.TButton", command=self.on_higher
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="Tiefer", style="Basic.TButton", command=self.on_lower
        ).pack(side="left", padx=5)

    def on_higher(self) -> None:
        if self.controller:
            self.controller.guess_higher()

    def on_lower(self) -> None:
        if self.controller:
            self.controller.guess_lower()

    def set_card(self, card: Card) -> None:
        if card.image is not None:
            self.card_label.config(text=card_text(card), image=card.image)
        else:
            self.card_label.config(text=card_text(card))

    def set_status(self, text: str) -> None:
        self.status_label.config(text=text)

    def set_score(self, score: int) -> None:
        self.score_label.config(text=f"Punkte: {score}")

    def show_result(self, result: str) -> None:
        window = tk.Toplevel(self)
        window.title("Spiel vorbei")
        ttk.Label(window, text=f"Game Over: {result}", font=BASIC_FONT, padding=10).pack()
        ttk.Button(window, text="Schließen", command=window.destroy).pack(pady=5)
