from games import load_builtin_games
from gameframework.gui.app import StartApp


def main() -> None:
    load_builtin_games()
    app = StartApp()
    app.mainloop()


if __name__ == "__main__":
    main()
