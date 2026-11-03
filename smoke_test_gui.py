"""GUI-Smoke-Test: baut StartApp und ein komplettes Spiel auf (braucht ein Display, z. B. xvfb-run)."""

import sys

from games import load_builtin_games
from gameframework.gui.app import GameApp, StartApp


def main() -> int:
    load_builtin_games()

    start = StartApp()
    start.update()
    start.destroy()

    app = GameApp("High/Low", options={"seed": 7, "max_rounds": 3})
    app.update()
    for _ in range(3):
        app.controller.guess_higher()
        app.update()
    assert app.model.is_game_over
    app.destroy()

    print("GUI smoke test OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
