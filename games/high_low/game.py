from gameframework.registry import register_game
from games.high_low.controller import HighLowController
from games.high_low.model import HighLowModel
from games.high_low.view import HighLowView


@register_game("High/Low", description="Ist die nächste Karte höher oder tiefer?")
class HighLowGame:
    model_class = HighLowModel
    view_class = HighLowView
    controller_class = HighLowController
