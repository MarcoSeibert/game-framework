from dataclasses import dataclass, field


@dataclass
class ModelEvent:
    """Ereignis, das ein Model an seine Observer meldet."""

    type: str
    data: dict = field(default_factory=dict)


class ModelObserver:
    def on_model_change(self, event: ModelEvent) -> None:
        """Wird aufgerufen, wenn sich das Model ändert."""
        raise NotImplementedError
