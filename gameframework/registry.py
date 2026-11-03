from dataclasses import dataclass
from typing import Callable


@dataclass
class GameDefinition:
    """Bündelt die MVC-Klassen eines registrierten Spiels."""

    name: str
    model_class: type
    view_class: type
    controller_class: type
    description: str = ""


GAME_REGISTRY: dict[str, GameDefinition] = {}


def register_game(name: str, description: str = "") -> Callable:
    """Dekorator: registriert eine Klasse mit model_class/view_class/controller_class."""

    def decorator(cls):
        GAME_REGISTRY[name] = GameDefinition(
            name=name,
            model_class=cls.model_class,
            view_class=cls.view_class,
            controller_class=cls.controller_class,
            description=description,
        )
        return cls

    return decorator


def get_game(name: str) -> GameDefinition:
    try:
        return GAME_REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"Unbekanntes Spiel {name!r}. Registriert: {sorted(GAME_REGISTRY)}"
        ) from None


def registered_games() -> dict[str, GameDefinition]:
    return dict(GAME_REGISTRY)
