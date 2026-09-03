"""Color palette / picker widget."""
import tkinter as tk
from tkinter import colorchooser

from PIL import Image, ImageDraw, ImageTk

#TODO -- option 0 in default palette ought to always match the canvas background
DEFAULT_PALETTE = [
    "#000000", "#555555", "#ff0000","#ffd900", "#00ff00", "#a800ad","#f57600",
    "#0000ff", "#979697", "#00ff00", "#FC9494", "#A19BFF","#f7ff81",
    "#aafafa",
]

SWATCH_SPRITE_SIZE = 16
SWATCH_PADDING = 6
SWATCH_PITCH = SWATCH_SPRITE_SIZE + SWATCH_PADDING
CURRENT_SPRITE_SIZE = 40
SPRITE_OUTLINE = "#333333"


def make_circle_sprite(color, size=SWATCH_SPRITE_SIZE, outline=SPRITE_OUTLINE, inset_ratio=0.15):
    """Render a circular color swatch as a PIL image using antialiased supersampling.

    `inset_ratio` controls how far the circle is inset from its square bounding
    box, as a fraction of `size`. A fixed pixel margin looks fine at large
    sizes but is imperceptible at small ones (the circle ends up filling the
    whole square), so the margin is scaled to size instead.
    """
    scale = 4
    big = size * scale
    image = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    margin = max(scale, int(big * inset_ratio))
    draw.ellipse((margin, margin, big - margin, big - margin), fill=color, outline=outline, width=scale)
    return image.resize((size, size), Image.LANCZOS)


class ColorPalette(tk.Frame):
    """Displays a wrapping grid of circular color-sprite swatches plus a custom color picker.

    Swatches are drawn as images directly on a Canvas (rather than square
    Label widgets), so only the circular sprite itself is visible with no
    surrounding square bounding box. Swatches wrap onto a new row after
    `columns` entries, so a palette of 10 colors with columns=8 renders as a
    row of 8 followed by a row of 2.
    """

    def __init__(self, master, on_color_selected, colors=None, columns=8, **kwargs):
        super().__init__(master, **kwargs)
        self.on_color_selected = on_color_selected
        self.colors = colors or DEFAULT_PALETTE
        self.columns = columns
        self.current_color = self.colors[0]

        # Keep references so PhotoImages aren't garbage-collected.
        self._swatch_sprites = []
        self._swatch_items = []  # list of (canvas_item_id, color)
        self._current_sprite = None
        self._current_item_id = None

        background = self.cget("bg")

        self.current_swatch = tk.Canvas(
            self, width=CURRENT_SPRITE_SIZE, height=CURRENT_SPRITE_SIZE,
            highlightthickness=0, bg=background,
        )
        self.current_swatch.grid(row=0, column=0, rowspan=2, padx=(0, 8), sticky="n")
        self._set_current_sprite(self.current_color)

        rows = -(-len(self.colors) // self.columns)  # ceil division
        self.swatch_canvas = tk.Canvas(
            self,
            width=self.columns * SWATCH_PITCH,
            height=rows * SWATCH_PITCH,
            highlightthickness=0,
            bg=background,
        )
        self.swatch_canvas.grid(row=0, column=1, sticky="w")
        self.swatch_canvas.bind("<Button-1>", self._on_swatch_canvas_click)

        for i, color in enumerate(self.colors):
            row, col = divmod(i, self.columns)
            cx = col * SWATCH_PITCH + SWATCH_PITCH / 2
            cy = row * SWATCH_PITCH + SWATCH_PITCH / 2
            sprite = ImageTk.PhotoImage(make_circle_sprite(color))
            self._swatch_sprites.append(sprite)
            item_id = self.swatch_canvas.create_image(cx, cy, image=sprite)
            self._swatch_items.append((item_id, color))

        custom_button = tk.Button(self, text="Custom...", command=self._pick_custom_color)
        custom_button.grid(row=1, column=1, sticky="w", pady=(4, 0))

    def _set_current_sprite(self, color):
        self._current_sprite = ImageTk.PhotoImage(make_circle_sprite(color, size=CURRENT_SPRITE_SIZE))
        if self._current_item_id is None:
            self._current_item_id = self.current_swatch.create_image(
                CURRENT_SPRITE_SIZE / 2, CURRENT_SPRITE_SIZE / 2, image=self._current_sprite
            )
        else:
            self.current_swatch.itemconfig(self._current_item_id, image=self._current_sprite)

    def _on_swatch_canvas_click(self, event):
        clicked = self.swatch_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not clicked:
            return
        clicked_id = clicked[-1]
        for item_id, color in self._swatch_items:
            if item_id == clicked_id:
                self._select_color(color)
                break

    def _select_color(self, color):
        self.current_color = color
        self._set_current_sprite(color)
        self.on_color_selected(color)


    def _pick_custom_color(self):
        color = colorchooser.askcolor(color=self.current_color, title="Choose color")[1]
        if color:
            self._select_color(color)
