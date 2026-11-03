from gameframework.core.cards import Card, Deck, create_standard_deck
from gameframework.core.events import ModelEvent
from gameframework.core.model import GameModel


class HighLowModel(GameModel):
    """High/Low: Ist die nächste Karte höher oder tiefer als die aktuelle?

    Optionen: "max_rounds" (Default 10), "seed" (für ein reproduzierbares Deck)
    oder "deck" (fertiges Deck, z. B. für Tests; wird dann nicht gemischt).
    Gleicher Rang zählt weder als höher noch als tiefer.
    """

    def __init__(self, options: dict = None) -> None:
        super().__init__(options)
        self.max_rounds = int(self.options.get("max_rounds", 10))
        deck = self.options.get("deck")
        if deck is not None:
            self.deck = deck
        else:
            self.deck = create_standard_deck(rng_seed=self.options.get("seed"))
            self.deck.shuffle()
        self._all_cards = list(self.deck.cards)
        self.current_card: Card | None = None
        self.score = 0
        self.round = 0
        self.last_guess: dict | None = None

    def start(self) -> None:
        self._draw_card()
        super().start()

    @property
    def is_game_over(self) -> bool:
        if self.current_card is None:
            return False
        return self.round >= self.max_rounds or self.deck.is_empty

    def result(self) -> str:
        return f"{self.score} von {self.round} Runden richtig (von {self.max_rounds} Runden)."

    def guess(self, direction: str) -> bool | None:
        """Rät 'higher' oder 'lower'; liefert True bei richtigem Tipp.

        Liefert None, wenn das Spiel bereits vorbei ist.
        """
        if self.is_game_over:
            return None
        if direction not in ("higher", "lower"):
            raise ValueError(
                f"Ungültige Richtung {direction!r} (erlaubt: 'higher', 'lower')."
            )
        if self.deck.is_empty:
            next_card, correct = None, False
        else:
            next_card = self.deck.draw()
            if direction == "higher":
                correct = next_card.rank > self.current_card.rank
            else:
                correct = next_card.rank < self.current_card.rank
        if correct:
            self.score += 1
        self.round += 1
        if next_card is not None:
            self.current_card = next_card
        self.last_guess = {"direction": direction, "card": next_card, "correct": correct}
        self.notify_observers(
            ModelEvent(
                "round_result",
                {
                    "card": next_card,
                    "correct": correct,
                    "score": self.score,
                    "round": self.round,
                    "max_rounds": self.max_rounds,
                    "deck_size": len(self.deck),
                },
            )
        )
        if self.is_game_over:
            self.notify_observers(ModelEvent("game_over", {"result": self.result()}))
        return correct

    def reset(self) -> None:
        self.deck = Deck(list(self._all_cards), rng=self.deck.rng)
        self.deck.shuffle()
        self.current_card = None
        self.score = 0
        self.round = 0
        self.last_guess = None
        self.start()

    def _draw_card(self) -> None:
        self.current_card = self.deck.draw()
        self.notify_observers(
            ModelEvent(
                "card_drawn",
                {
                    "card": self.current_card,
                    "round": self.round,
                    "score": self.score,
                    "deck_size": len(self.deck),
                },
            )
        )
