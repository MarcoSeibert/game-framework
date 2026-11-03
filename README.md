# Game Framework

Ein kleines Python-Framework, um **unterschiedliche Kartenspiele oder einfache Brettspiele** im **MVC-Muster** zu entwickeln – inklusive einer **GUI auf Basis von tkinter**.

Es werden ausschließlich die Python-Standardbibliothek und tkinter verwendet; es gibt **keine externen Abhängigkeiten**.

## Voraussetzungen

- Python >= 3.10
- tkinter (Bestandteil der Standardbibliothek; unter Linux ggf. das Paket `python3-tk` installieren)
- ein Display für die GUI (die Spiellogik und alle Tests laufen auch headless)

## Quickstart

```bash
python main.py
```

Es öffnet sich ein Startmenü mit allen registrierten Spielen (mitgeliefert: **High/Low**). Spiel auswählen, auf „Spielen!“ klicken – fertig.

## Architektur (MVC + Observer)

```
main.py ──► StartApp (Spielauswahl)
               │  startet GameApp
               ▼
        GameApp verdrahtet die drei Schichten:

   ┌─────────┐   Events (ModelEvent)   ┌────────────┐
   │  Model  │ ───────────────────────► │ Controller │ ── Methodenaufrufe ──► ┌───────┐
   │ (Logik) │ ◄── Methodenaufrufe ──── │ (Vermittler)│ ◄── Klicks/Buttons ─── │ View  │
   └─────────┘                         └────────────┘                          └───────┘
        ▲                                                                    (tkinter)
        └──────── Observer registriert sich am Model ◄────────────────────────┘
```

- **Model** (`gameframework/core/`): reine Spiellogik – kennt weder tkinter noch die View. Änderungen werden als `ModelEvent` an registrierte Observer gemeldet.
- **Controller** (`gameframework/mvc/controller.py`): lauscht auf Model-Events (`on_<event.type>`-Handler) und ruft View-Methoden auf; GUI-Aktionen rufen Controller-Methoden auf, die das Model verändern.
- **View** (`gameframework/gui/`): tkinter-Widgets, rendert den Model-Zustand und leitet Benutzereingaben an den Controller weiter.
- **Registry** (`gameframework/registry.py`): Spiele melden sich per `@register_game("Name")` an; `main.py` listet automatisch alle registrierten Spiele.

Der Kern (`gameframework/core`, `gameframework/mvc`, `registry`) importiert **kein tkinter** und ist damit ohne Display testbar.

## Neues Spiel hinzufügen

Ein Spiel besteht aus drei Klassen in einem eigenen Paket unter `games/<name>/` plus einer Registrierungsdatei:

```
games/meinspiel/
├── __init__.py        (leer)
├── model.py           (erbt GameModel)
├── controller.py      (erbt BaseController)
├── view.py            (erbt BaseView)
└── game.py            (registriert das Spiel)
```

**1. Model** – Logik und Events:

```python
# games/meinspiel/model.py
from gameframework import GameModel, ModelEvent

class MeinSpielModel(GameModel):
    def __init__(self, options=None):
        super().__init__(options)
        self.versuche = 0
        self.fertig = False

    @property
    def is_game_over(self):
        return self.fertig

    def rate(self):
        self.versuche += 1
        self.fertig = self.versuche >= 3
        self.notify_observers(ModelEvent("zug", {"versuche": self.versuche}))
        if self.fertig:
            self.notify_observers(ModelEvent("game_over", {"result": self.result()}))

    def result(self):
        return f"{self.versuche} Versuche gebraucht."
```

**2. Controller** – Events empfangen, Aktionen entgegennehmen:

```python
# games/meinspiel/controller.py
from gameframework import BaseController, ModelEvent

class MeinSpielController(BaseController):
    def on_button_click(self):
        self.model.rate()

    def on_zug(self, event: ModelEvent):
        self.view.set_status(f"Versuch {event.data['versuche']}")

    def on_game_over(self, event: ModelEvent):
        self.view.show_result(event.data["result"])
```

**3. View** – tkinter-Widgets:

```python
# games/meinspiel/view.py
from tkinter import ttk
from gameframework.gui.base_view import BaseView
from gameframework.gui.theme import BASIC_FONT

class MeinSpielView(BaseView):
    def __init__(self, parent):
        super().__init__(parent, title="Mein Spiel")
        self.status = ttk.Label(self, text="", font=BASIC_FONT)
        self.status.pack(pady=10)
        ttk.Button(self, text="Raten!", font=BASIC_FONT,
                   command=self.on_button).pack()

    def on_button(self):
        if self.controller:
            self.controller.on_button_click()

    def set_status(self, text):
        self.status.config(text=text)

    def show_result(self, result):
        self.set_status(f"Game Over: {result}")
```

**4. Registrieren:**

```python
# games/meinspiel/game.py
from gameframework import register_game
from games.meinspiel.model import MeinSpielModel
from games.meinspiel.view import MeinSpielView
from games.meinspiel.controller import MeinSpielController

@register_game("Mein Spiel", description="Kurzes Demispiel")
class MeinSpielGame:
    model_class = MeinSpielModel
    view_class = MeinSpielView
    controller_class = MeinSpielController
```

```python
# games/__init__.py  –  das neue Spiel in load_builtin_games() importieren:
def load_builtin_games():
    from games.high_low.game import HighLowGame  # noqa: F401
    from games.meinspiel.game import MeinSpielGame  # noqa: F401
```

Beim nächsten `python main.py` erscheint das Spiel automatisch im Startmenü.

## Kartenspiele

- `Card`: ID, Name, optionaler `rank`/`suit` (zum Vergleichen) und optionale Bilder (`front_image`/`back_image`, z. B. `tkinter.PhotoImage`); `flip()` dreht die Karte.
- `Deck`: `shuffle()`, `draw()`, `draw_many(n)`, `peek(n)`, `discard()`, `EmptyDeckError` bei leerem Deck. Der Zufallsgenerator ist injizierbar (seedbar für Tests).
- `create_standard_deck(rng_seed=...)`: Standard-52-Karten-Deck.
- GUI-Hilfen: `gameframework/gui/card_view.py` (`make_card_label`, `make_card_button`, `card_text`).

## Brettspiele

- `Board(rows, cols)`: generisches Grid mit `get`/`set`/`is_empty`/`cells`/`clear` und `IndexError` außerhalb des Bretts.
- `BoardView(parent, board, cell_size=...)`: Canvas-Grid; Klicks rufen `controller.on_board_click(row, col)` auf; Zellen mit `draw_cell(row, col, text, fill)` zeichnen.
- Spielfeldlogik (z. B. TicTacToe) liegt im Model auf einem `Board`, die Validierung im Controller.

## Tests

```bash
python -m unittest discover -v
```

Alle Tests laufen ohne Display (nur der GUI-freie Kern wird getestet). Zum Syntax-Check der GUI-Dateien genügt `python -m compileall gameframework games main.py`.

## Projektstruktur

```
main.py                     Einstiegspunkt (Startmenü)
gameframework/
├── core/                   GUI-unabhängiger Kern
│   ├── events.py           ModelEvent, ModelObserver
│   ├── model.py            GameModel (Spieler, Observer, Events)
│   ├── cards.py            Card, Deck, create_standard_deck()
│   └── board.py            Board (Grid für Brettspiele)
├── mvc/
│   └── controller.py       BaseController (Event-Dispatch, on_board_click)
├── gui/                    tkinter-View-Schicht
│   ├── app.py              GameApp (verdrahtet MVC), StartApp (Menü)
│   ├── base_view.py        BaseView (Menüleiste, Titel)
│   ├── card_view.py        Karten-Label/-Button
│   ├── board_view.py       BoardView (Canvas-Grid)
│   └── theme.py            Fonts/Konstanten
└── registry.py             @register_game, GAME_REGISTRY
games/high_low/             Beispiel-Kartenspiel (Model/Controller/View/Game)
tests/                      unittest-Suite (headless)
```
