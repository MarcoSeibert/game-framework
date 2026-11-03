from tkinter import ttk

from gameframework.core.cards import Card
from gameframework.gui.theme import CARD_FONT


def card_text(card: Card) -> str:
    """Anzeigetext einer Karte (Name, sonst ID)."""
    return card.name or str(card.card_id)


def make_card_label(parent, card: Card, **kwargs) -> ttk.Label:
    """Erzeugt ein Label für eine Karte; nutzt card.image, falls gesetzt."""
    kwargs.setdefault("text", card_text(card))
    kwargs.setdefault("font", CARD_FONT)
    label = ttk.Label(parent, **kwargs)
    if card.image is not None:
        label.config(image=card.image)
    return label


def make_card_button(parent, card: Card, command, **kwargs) -> ttk.Button:
    """Erzeugt einen klickbaren Button für eine Karte; command(card) wird aufgerufen."""
    kwargs.setdefault("text", card_text(card))
    button = ttk.Button(parent, command=lambda: command(card), **kwargs)
    if card.image is not None:
        button.config(image=card.image)
    return button
