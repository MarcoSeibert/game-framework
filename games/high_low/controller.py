from gameframework.core.events import ModelEvent
from gameframework.mvc.controller import BaseController


class HighLowController(BaseController):
    """Verbindet HighLowModel und HighLowView über Events und Button-Aktionen."""

    def guess_higher(self) -> None:
        self.model.guess("higher")

    def guess_lower(self) -> None:
        self.model.guess("lower")

    def on_card_drawn(self, event: ModelEvent) -> None:
        self.view.set_card(event.data["card"])
        self.view.set_status(
            f"Runde {event.data['round'] + 1} von {self.model.max_rounds}"
        )
        self.view.set_score(event.data["score"])

    def on_round_result(self, event: ModelEvent) -> None:
        data = event.data
        if data["card"] is not None:
            self.view.set_card(data["card"])
        self.view.set_score(data["score"])
        verdict = "Richtig!" if data["correct"] else "Falsch!"
        self.view.set_status(f"{verdict} – Runde {data['round']}/{data['max_rounds']}")

    def on_game_over(self, event: ModelEvent) -> None:
        self.view.show_result(event.data["result"])
