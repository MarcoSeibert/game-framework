def load_builtin_games() -> None:
    """Importiert die mitgelieferten Spiele, damit sie sich in der Registry anmelden."""
    from games.high_low.game import HighLowGame  # noqa: F401
