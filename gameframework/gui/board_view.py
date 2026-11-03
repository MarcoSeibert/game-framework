import tkinter as tk

from gameframework.core.board import Board
from gameframework.gui.base_view import BaseView


class BoardView(BaseView):
    """Canvas-basierte Grid-Ansicht für Brettspiele.

    Klicks auf Zellen werden an controller.on_board_click(row, col) weitergereicht.
    """

    def __init__(
        self,
        parent: tk.Tk,
        board: Board,
        cell_size: int = 60,
        title: str = "",
        bg: str = "white",
    ) -> None:
        super().__init__(parent, title=title)
        self.board = board
        self.cell_size = cell_size
        self.canvas = tk.Canvas(
            self,
            width=board.cols * cell_size,
            height=board.rows * cell_size,
            bg=bg,
            highlightthickness=0,
        )
        self.canvas.pack(pady=10, padx=10)
        self.canvas.bind("<Button-1>", self._on_click)
        self._cells: dict = {}

    def _on_click(self, event) -> None:
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if self.board.in_bounds(row, col) and self.controller is not None:
            self.controller.on_board_click(row, col)

    def draw_cell(self, row: int, col: int, text: str = "", fill: str = "white") -> None:
        """Zeichnet oder aktualisiert eine Zelle."""
        x0, y0 = col * self.cell_size, row * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        key = (row, col)
        if key in self._cells:
            rect, text_id = self._cells[key]
            self.canvas.itemconfig(rect, fill=fill)
            self.canvas.itemconfig(text_id, text=text)
        else:
            rect = self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=fill, outline="grey"
            )
            text_id = self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=text)
            self._cells[key] = (rect, text_id)

    def clear_board(self) -> None:
        self.canvas.delete("all")
        self._cells.clear()
