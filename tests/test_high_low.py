import unittest

from gameframework.core.cards import Card, Deck
from games.high_low.model import HighLowModel


def make_model(ranks, max_rounds=3):
    """Deck mit bekannten Rängen; draw() nimmt die letzte Karte zuerst."""
    cards = [Card(f"c{i}", name=f"Karte {r}", rank=r) for i, r in enumerate(ranks)]
    return HighLowModel({"deck": Deck(cards), "max_rounds": max_rounds})


class RecordingObserver:
    def __init__(self):
        self.events = []

    def on_model_change(self, event):
        self.events.append(event)


class TestHighLowModel(unittest.TestCase):
    def test_start_draws_first_card_and_notifies(self):
        model = make_model([5, 10, 3, 7])
        observer = RecordingObserver()
        model.add_observer(observer)
        model.start()
        self.assertEqual(model.current_card.rank, 7)
        self.assertEqual(
            [e.type for e in observer.events], ["card_drawn", "game_started"]
        )

    def test_full_game_flow(self):
        model = make_model([5, 10, 3, 7], max_rounds=2)
        observer = RecordingObserver()
        model.add_observer(observer)
        model.start()
        self.assertFalse(model.is_game_over)
        self.assertTrue(model.guess("lower"))
        self.assertTrue(model.guess("higher"))
        self.assertTrue(model.is_game_over)
        self.assertIsNone(model.guess("higher"))
        self.assertEqual(model.score, 2)
        self.assertEqual(model.round, 2)
        self.assertEqual(
            [e.type for e in observer.events],
            ["card_drawn", "game_started", "round_result", "round_result", "game_over"],
        )
        self.assertIn("2 von 2", model.result())

    def test_wrong_guess_scores_nothing(self):
        model = make_model([5, 10, 3, 7], max_rounds=1)
        model.start()
        self.assertFalse(model.guess("higher"))
        self.assertEqual(model.score, 0)
        self.assertEqual(model.round, 1)
        self.assertTrue(model.is_game_over)

    def test_equal_rank_is_neither_higher_nor_lower(self):
        model = make_model([8, 8], max_rounds=2)
        model.start()
        self.assertFalse(model.guess("higher"))
        self.assertFalse(model.guess("lower"))
        self.assertTrue(model.is_game_over)
        self.assertEqual(model.score, 0)

    def test_invalid_direction_raises(self):
        model = make_model([5, 10])
        model.start()
        with self.assertRaises(ValueError):
            model.guess("sideways")

    def test_seeded_standard_deck_game(self):
        model = HighLowModel({"seed": 123, "max_rounds": 10})
        model.start()
        for _ in range(10):
            model.guess("higher")
        self.assertTrue(model.is_game_over)
        self.assertEqual(model.round, 10)
        self.assertGreaterEqual(model.score, 0)
        self.assertLessEqual(model.score, 10)

    def test_reset_restarts_game(self):
        model = make_model([5, 10, 3, 7], max_rounds=2)
        model.start()
        model.guess("lower")
        model.guess("higher")
        self.assertTrue(model.is_game_over)
        model.reset()
        self.assertFalse(model.is_game_over)
        self.assertEqual(model.score, 0)
        self.assertEqual(model.round, 0)
        self.assertIsNotNone(model.current_card)
        self.assertEqual(len(model.deck), 3)
