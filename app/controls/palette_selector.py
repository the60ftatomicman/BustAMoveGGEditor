from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk,colorchooser
from app.controls.section import section
from PIL import Image, ImageDraw, ImageTk

SWATCH_SPRITE_SIZE  = 16
SWATCH_PADDING      = 6
SWATCH_PITCH        = SWATCH_SPRITE_SIZE + SWATCH_PADDING
CURRENT_SPRITE_SIZE = 40
DEFAULT_PALETTE = [
    "#000000", "#000000", "#000000","#000000", "#000000", "#000000","#000000",
    "#000000", "#000000", "#000000", "#000000", "#000000","#000000",
    "#000000",
]

##
## What I want out of this is:
## 1) to be able to use an rgb selector for the palettes

class palette_selector(section):
    def __init__(self,parentFrame:tk.Frame=None,r:int=0,c:int=0):
        super().__init__(name=self.__class__.__name__,parentFrame=parentFrame,r=r,c=c)
        self.element       = None
        # Tk doesn't retain Python references to images used by Canvas items.
        # Keep the PhotoImages alive for as long as the palette is displayed.
        self._sprites      = []
        self.colors        = DEFAULT_PALETTE
        self.current_color = self.colors[0]

        tk.Label(self.frame, text="Palette").grid(row=0, column=0)
        self.current = tk.Canvas(
            self.frame, 
            width = SWATCH_PITCH, 
            height= SWATCH_PITCH,
            highlightthickness=1,
            bg=self.current_color
        )
        self.current.grid(row=0, column=1, padx=(0, 0))

        self.element = tk.Canvas(
            self.frame, 
            width = SWATCH_PITCH, 
            height= SWATCH_PITCH * len(self.colors) + SWATCH_PADDING,
            highlightthickness=0
        )
        self.element.grid(row=1, column=0, padx=(0, 8))
        self.set_colors()


    def _generate_sprite(self,color):
        image = Image.new("RGBA", (SWATCH_SPRITE_SIZE, SWATCH_SPRITE_SIZE), (0, 0, 0, 0))
        draw  = ImageDraw.Draw(image)
        draw.rectangle(xy=(0,0,SWATCH_SPRITE_SIZE,SWATCH_SPRITE_SIZE),fill=color)
        return image

    def set_colors(self,colorlist:list=None):
        if colorlist != None:
            self.colors = []
            for c in colorlist:
                self.colors.append(c.color.toRGBHEX())
                
        self.element.delete("all")
        self._sprites = []
        for i, color in enumerate(self.colors):
            cx = SWATCH_PADDING
            cy = (i*SWATCH_PITCH)+SWATCH_PADDING
            sprite = ImageTk.PhotoImage(self._generate_sprite(color))
            self._sprites.append(sprite)
            self.element.create_image(cx, cy, image=sprite)

        self.current_color = self.colors[0]
        self.current.config(bg=self.current_color)

    def _edit_selected_color(self):
        color = colorchooser.askcolor(color=self.current_color, title="Choose color")[1]
        if color:
            self._select_color(color)