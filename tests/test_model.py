import unittest

from gameframework.core.events import ModelEvent
from gameframework.core.model import GameModel


class RecordingObserver:
    def __init__(self):
        self.events = []

    def on_model_change(self, event):
        self.events.append(event)


class TestGameModel(unittest.TestCase):
    def test_observer_notification(self):
        model = GameModel()
        observer = RecordingObserver()
        model.add_observer(observer)
        model.notify_observers(ModelEvent("test", {"a": 1}))
        self.assertEqual(len(observer.events), 1)
        self.assertEqual(observer.events[0].type, "test")
        self.assertEqual(observer.events[0].data, {"a": 1})

    def test_remove_observer(self):
        model = GameModel()
        observer = RecordingObserver()
        model.add_observer(observer)
        model.remove_observer(observer)
        model.notify_observers(ModelEvent("test"))
        self.assertEqual(observer.events, [])

    def test_player_rotation(self):
        model = GameModel({"players": ["A", "B"]})
        self.assertEqual(model.current_player, "A")
        model.next_player()
        self.assertEqual(model.current_player, "B")
        model.next_player()
        self.assertEqual(model.current_player, "A")

    def test_next_player_notifies(self):
        model = GameModel({"players": ["A", "B"]})
        observer = RecordingObserver()
        model.add_observer(observer)
        model.next_player()
        self.assertEqual(observer.events[0].type, "player_changed")
        self.assertEqual(observer.events[0].data["player"], "B")

    def test_defaults(self):
        model = GameModel()
        self.assertEqual(model.players, ["Spieler 1"])
        self.assertFalse(model.is_game_over)
        self.assertIsNone(model.result())

    def test_start_notifies_game_started(self):
        model = GameModel({"players": ["A"]})
        observer = RecordingObserver()
        model.add_observer(observer)
        model.start()
        self.assertEqual(observer.events[0].type, "game_started")
        self.assertEqual(observer.events[0].data["players"], ["A"])

    def test_reset_not_implemented_in_base(self):
        with self.assertRaises(NotImplementedError):
            GameModel().reset()
