import random
import unittest

from gameframework.core.cards import Card, Deck, EmptyDeckError, create_standard_deck


class TestCard(unittest.TestCase):
    def test_flip_changes_image_side(self):
        front, back = object(), object()
        card = Card("1", front_image=front, back_image=back)
        self.assertIs(card.image, front)
        card.flip()
        self.assertIs(card.image, back)
        card.flip()
        self.assertIs(card.image, front)

    def test_repr_contains_name(self):
        self.assertIn("Ass Herz", repr(Card("14_Herz", name="Ass Herz")))


class TestStandardDeck(unittest.TestCase):
    def test_has_52_unique_cards(self):
        deck = create_standard_deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(len({c.card_id for c in deck.cards}), 52)
        self.assertTrue(all(c.rank is not None and c.suit is not None for c in deck.cards))

    def test_seeded_deck_shuffles_deterministically(self):
        deck_a = create_standard_deck(rng_seed=42)
        deck_b = create_standard_deck(rng_seed=42)
        deck_a.shuffle()
        deck_b.shuffle()
        self.assertEqual(
            [c.card_id for c in deck_a.cards], [c.card_id for c in deck_b.cards]
        )


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck([Card(str(i), rank=i) for i in range(1, 6)], rng=random.Random(1))

    def test_draw_pops_from_top(self):
        self.assertEqual(self.deck.draw().rank, 5)
        self.assertEqual(len(self.deck), 4)

    def test_draw_from_empty_deck_raises(self):
        with self.assertRaises(EmptyDeckError):
            Deck().draw()

    def test_draw_many(self):
        drawn = self.deck.draw_many(3)
        self.assertEqual([c.rank for c in drawn], [5, 4, 3])
        self.assertEqual(len(self.deck), 2)

    def test_peek_does_not_remove(self):
        top = self.deck.peek(2)
        self.assertEqual([c.rank for c in top], [4, 5])
        self.assertEqual(len(self.deck), 5)

    def test_add_and_discard(self):
        card = Card("x", rank=99)
        self.deck.add(card)
        self.assertIs(self.deck.draw(), card)
        self.deck.discard(card)
        self.assertEqual(self.deck.discard_pile, [card])

    def test_is_empty(self):
        self.assertFalse(self.deck.is_empty)
        self.assertTrue(Deck().is_empty)
