"""Pixel grid canvas widget built on tkinter Canvas.

Displays a rows x columns grid of cells (each dimension is expected to be a
multiple of 8) that the user can click, or click-and-drag, to paint with the
currently selected color. Rows and columns may differ, so the grid does not
need to be square.

The grid is "askewed": odd rows (1-indexed: 1, 3, 5, ...) contain the full
`columns` count, while even rows (1-indexed: 2, 4, 6, ...) contain one fewer
column and are indented by half a cell width, giving a brick-like offset
layout.
"""
import tkinter as tk


class PixelGridCanvas(tk.Canvas):
    """A tkinter Canvas that renders and manages an editable pixel grid."""

    DEFAULT_BG_COLOR     = "#000000"
    DEFAULT_OUTLINE_COLOR = "#6B015D"
    DEFAULT_CANVAS_BG_COLOR = "#333333"
    
    def __init__(self, master, rows=10, columns=10, cell_size=16, bg_color=DEFAULT_BG_COLOR,
                 outline_color=DEFAULT_OUTLINE_COLOR, canvas_bg_color=DEFAULT_CANVAS_BG_COLOR, **kwargs):
        width  = columns * cell_size
        height = rows    * cell_size
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=canvas_bg_color, **kwargs)

        self.rows          = rows
        self.columns       = columns
        self.cell_size     = cell_size
        self.default_color = bg_color
        self.current_color = "#000000"
        self.outline_color = outline_color

        # cell_colors[row][col] -> hex color string currently painted
        # (rows have varying lengths; see _row_columns)
        self.cell_colors = [[self.default_color for _ in range(self._row_columns(row))] for row in range(rows)]
        # cell_ids[row][col] -> canvas rectangle item id
        self.cell_ids = [[None for _ in range(self._row_columns(row))] for row in range(rows)]

        self._draw_grid()

        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_click)

    def _row_columns(self, row):
        """Number of columns in the given 0-indexed row.

        Even indices (1-indexed odd rows) get the full column count; odd
        indices (1-indexed even rows) get one fewer column.
        """
        return self.columns if row % 2 == 0 else self.columns - 1

    def _row_offset(self, row):
        """X pixel offset applied to the given 0-indexed row."""
        return 0 if row % 2 == 0 else self.cell_size // 2

    def _draw_grid(self):
        self.delete("all")
        for row in range(self.rows):
            offset = self._row_offset(row)
            for col in range(self._row_columns(row)):
                x0 = offset + col * self.cell_size
                y0 = row * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                color = self.cell_colors[row][col]
                cell_id = self.create_rectangle(x0, y0, x1, y1, fill=color, outline=self.outline_color)
                self.cell_ids[row][col] = cell_id

    def _on_click(self, event):
        row = event.y // self.cell_size
        if not (0 <= row < self.rows):
            return
        offset = self._row_offset(row)
        col = (event.x - offset) // self.cell_size
        if 0 <= col < self._row_columns(row):
            self.paint_cell(row, int(col), self.current_color)

    def paint_cell(self, row, col, color):
        """Set the color of a single cell, updating both state and canvas."""
        self.cell_colors[row][col] = color
        cell_id = self.cell_ids[row][col]
        if cell_id is not None:
            self.itemconfig(cell_id, fill=color)

    def set_current_color(self, color):
        """Set the color that will be used for subsequent clicks."""
        self.current_color = color

    def set_outline_color(self, color):
        """Change the outline color drawn around every cell."""
        self.outline_color = color
        self._draw_grid()

    def set_canvas_bg_color(self, color):
        """Change the canvas's own background color (shown around/between cells)."""
        self.config(bg=color)

    def clear(self, color=None):
        """Reset every cell to `color` (or the canvas default)."""
        color = color or self.default_color
        for row in range(self.rows):
            for col in range(self._row_columns(row)):
                self.paint_cell(row, col, color)

    def resize_grid(self, rows, columns, cell_size=None):
        """Rebuild the grid at a new size, discarding current painted state."""
        self.rows = rows
        self.columns = columns
        if cell_size is not None:
            self.cell_size = cell_size
        self.cell_colors = [[self.default_color for _ in range(self._row_columns(row))] for row in range(rows)]
        self.cell_ids = [[None for _ in range(self._row_columns(row))] for row in range(rows)]
        self.config(width=columns * self.cell_size, height=rows * self.cell_size)
        self._draw_grid()

    def to_image(self):
        """Render the current grid to a PIL Image (one pixel per cell).

        Since even rows are indented by half a cell, this doubles the
        horizontal resolution so the offset can be represented as a whole
        pixel shift.
        """
        from PIL import Image

        image = Image.new("RGB", (self.columns * 2, self.rows), self.default_color)
        pixels = image.load()
        for row in range(self.rows):
            shift = 0 if row % 2 == 0 else 1
            for col, color in enumerate(self.cell_colors[row]):
                rgb = self._hex_to_rgb(color)
                x = shift + col * 2
                pixels[x, row] = rgb
                pixels[x + 1, row] = rgb
        return image

    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

