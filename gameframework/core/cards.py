import random

SUITS = ("Herz", "Karo", "Kreuz", "Pik")
RANK_NAMES = {11: "Bube", 12: "Dame", 13: "König", 14: "Ass"}


class EmptyDeckError(Exception):
    """Wird ausgelöst, wenn aus einem leeren Deck gezogen werden soll."""


class Card:
    """Eine Karte mit optionalem Rang/einer Farbe und optionalen Bildern (z. B. PhotoImage)."""

    def __init__(
        self,
        card_id: int | str,
        name: str = "",
        rank: int | None = None,
        suit: str | None = None,
        front_image=None,
        back_image=None,
    ) -> None:
        self.card_id = card_id
        self.name = name
        self.rank = rank
        self.suit = suit
        self.front_image = front_image
        self.back_image = back_image
        self.face_up = True

    def flip(self) -> None:
        """Dreht die Karte um."""
        self.face_up = not self.face_up

    @property
    def image(self):
        """Aktuell sichtbares Bild abhängig von der Orientierung."""
        return self.front_image if self.face_up else self.back_image

    def __repr__(self) -> str:
        return f"Card({self.card_id!r}, name={self.name!r})"


class Deck:
    """Ein Stapel von Karten; die oberste Karte liegt am Ende der Liste."""

    def __init__(self, cards: list | None = None, rng: random.Random | None = None) -> None:
        self.cards = list(cards) if cards else []
        self.rng = rng if rng is not None else random.Random()
        self.discard_pile: list[Card] = []

    def shuffle(self) -> None:
        """Mischt den Stapel mit dem eigenen Zufallsgenerator (für Tests seedbar)."""
        self.rng.shuffle(self.cards)

    def draw(self) -> Card:
        """Zieht die oberste Karte; wirft EmptyDeckError bei leerem Deck."""
        if not self.cards:
            raise EmptyDeckError("Das Deck ist leer.")
        return self.cards.pop()

    def draw_many(self, n: int) -> list:
        return [self.draw() for _ in range(n)]

    def add(self, card: Card) -> None:
        """Legt eine Karte oben auf den Stapel."""
        self.cards.append(card)

    def discard(self, card: Card) -> None:
        """Legt eine Karte auf den Ablagestapel."""
        self.discard_pile.append(card)

    def peek(self, n: int = 1) -> list:
        """Blickt auf die obersten n Karten, ohne sie zu ziehen."""
        return self.cards[-n:]

    @property
    def is_empty(self) -> bool:
        return not self.cards

    def __len__(self) -> int:
        return len(self.cards)


def create_standard_deck(rng_seed: int | None = None) -> Deck:
    """Erzeugt ein Standard-52-Karten-Deck (2–10, Bube, Dame, König, Ass in 4 Farben)."""
    rng = random.Random(rng_seed)
    cards = []
    for suit in SUITS:
        for rank in range(2, 15):
            name = f"{RANK_NAMES.get(rank, str(rank))} {suit}"
            cards.append(Card(card_id=f"{rank}_{suit}", name=name, rank=rank, suit=suit))
    return Deck(cards, rng=rng)
