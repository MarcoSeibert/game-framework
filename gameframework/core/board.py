class Board:
    """Generisches rechteckiges Grid für Brettspiele; Zellen beginnen leer (None)."""

    def __init__(self, rows: int, cols: int, fill=None) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = [[fill for _ in range(cols)] for _ in range(rows)]

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get(self, row: int, col: int):
        self._check(row, col)
        return self.grid[row][col]

    def set(self, row: int, col: int, value) -> None:
        self._check(row, col)
        self.grid[row][col] = value

    def is_empty(self, row: int, col: int) -> bool:
        return self.get(row, col) is None

    def cells(self):
        """Iteriert über alle Zellen als (row, col, value)."""
        for row in range(self.rows):
            for col in range(self.cols):
                yield row, col, self.grid[row][col]

    def clear(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = None

    def _check(self, row: int, col: int) -> None:
        if not self.in_bounds(row, col):
            raise IndexError(
                f"Feld ({row}, {col}) liegt außerhalb des Bretts ({self.rows}x{self.cols})."
            )
