from gameframework.core.events import ModelEvent, ModelObserver


class GameModel:
    """Basis-MVC-Model: verwaltet Spieler und Observer und meldet Änderungen als Events."""

    def __init__(self, options: dict = None) -> None:
        self.options = options if options else {}
        self.players = list(self.options.get("players", ["Spieler 1"]))
        self.current_player_index = 0
        self.observers: list[ModelObserver] = []

    def add_observer(self, observer: ModelObserver) -> None:
        """Fügt einen Observer hinzu (z. B. den Controller)."""
        self.observers.append(observer)

    def remove_observer(self, observer: ModelObserver) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, event: ModelEvent) -> None:
        """Benachrichtigt alle Observer über ein Event."""
        for observer in list(self.observers):
            observer.on_model_change(event)

    @property
    def current_player(self) -> str:
        return self.players[self.current_player_index]

    def next_player(self) -> None:
        """Gibt den Zug an den nächsten Spieler weiter."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.notify_observers(
            ModelEvent("player_changed", {"player": self.current_player})
        )

    @property
    def is_game_over(self) -> bool:
        return False

    def result(self) -> str | None:
        """Ergebnis-Text nach Spielende; None solange das Spiel läuft."""
        return None

    def start(self) -> None:
        """Wird nach dem Verdrahten von Model/View/Controller aufgerufen."""
        self.notify_observers(
            ModelEvent("game_started", {"players": list(self.players)})
        )

    def reset(self) -> None:
        """Setzt das Spiel zurück; in Unterklassen überschreiben."""
        raise NotImplementedError
