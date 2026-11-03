import unittest

from gameframework.registry import GAME_REGISTRY, get_game, register_game, registered_games


class DummyGame:
    model_class = view_class = controller_class = object


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self._backup = dict(GAME_REGISTRY)

    def tearDown(self):
        GAME_REGISTRY.clear()
        GAME_REGISTRY.update(self._backup)

    def test_register_and_get(self):
        register_game("Dummy", description="Testspiel")(DummyGame)
        definition = get_game("Dummy")
        self.assertEqual(definition.name, "Dummy")
        self.assertIs(definition.model_class, object)
        self.assertEqual(definition.description, "Testspiel")
        self.assertIn("Dummy", registered_games())

    def test_unknown_game_raises_key_error(self):
        with self.assertRaises(KeyError):
            get_game("gibt es nicht")
