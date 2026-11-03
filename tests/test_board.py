import unittest

from gameframework.core.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(3, 4)

    def test_initial_cells_are_empty(self):
        cells = list(self.board.cells())
        self.assertEqual(len(cells), 12)
        self.assertTrue(all(self.board.is_empty(r, c) for r, c, _ in cells))

    def test_set_and_get(self):
        self.board.set(1, 2, "X")
        self.assertEqual(self.board.get(1, 2), "X")
        self.assertFalse(self.board.is_empty(1, 2))

    def test_out_of_bounds_raises(self):
        with self.assertRaises(IndexError):
            self.board.get(3, 0)
        with self.assertRaises(IndexError):
            self.board.set(0, 4, "X")
        self.assertFalse(self.board.in_bounds(-1, 0))
        self.assertFalse(self.board.in_bounds(0, 4))
        self.assertTrue(self.board.in_bounds(2, 3))

    def test_clear(self):
        self.board.set(0, 0, "X")
        self.board.set(2, 3, "O")
        self.board.clear()
        self.assertTrue(self.board.is_empty(0, 0))
        self.assertTrue(self.board.is_empty(2, 3))
