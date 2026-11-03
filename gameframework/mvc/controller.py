from gameframework.core.events import ModelEvent, ModelObserver
from gameframework.core.model import GameModel


class BaseController(ModelObserver):
    """Basis-Controller: empfängt Model-Events und verteilt sie an on_<event.type>-Handler.

    GUI-Events (Klicks, Buttons) rufen Methoden des Controllers auf, der wiederum
    das Model verändert. Das Model kennt weder View noch tkinter.
    """

    def __init__(self, model: GameModel, view=None) -> None:
        self.model = model
        self.view = view
        self.model.add_observer(self)

    def set_view(self, view) -> None:
        self.view = view

    def on_model_change(self, event: ModelEvent) -> None:
        handler = getattr(self, f"on_{event.type}", None)
        if handler is not None:
            handler(event)

    def on_board_click(self, row: int, col: int) -> None:
        """Hook für Brettspiele; in Unterklassen überschreiben."""
