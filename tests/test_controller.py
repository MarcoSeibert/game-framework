import unittest

from gameframework.core.events import ModelEvent
from gameframework.core.model import GameModel
from gameframework.mvc.controller import BaseController


class RecordingController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.seen = []

    def on_custom_event(self, event):
        self.seen.append(event)


class TestBaseController(unittest.TestCase):
    def test_controller_registers_as_observer(self):
        model = GameModel()
        controller = RecordingController(model)
        self.assertIn(controller, model.observers)

    def test_dispatches_event_to_matching_handler(self):
        model = GameModel()
        controller = RecordingController(model)
        model.notify_observers(ModelEvent("custom_event", {"x": 1}))
        self.assertEqual(len(controller.seen), 1)
        self.assertEqual(controller.seen[0].data, {"x": 1})

    def test_unknown_event_type_is_ignored(self):
        model = GameModel()
        controller = RecordingController(model)
        model.notify_observers(ModelEvent("something_else"))
        self.assertEqual(controller.seen, [])

    def test_on_board_click_default_is_noop(self):
        controller = BaseController(GameModel())
        controller.on_board_click(0, 0)

    def test_set_view(self):
        controller = BaseController(GameModel())
        view = object()
        controller.set_view(view)
        self.assertIs(controller.view, view)
