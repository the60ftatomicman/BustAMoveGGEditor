from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk,colorchooser
from app.controls.section import section
from PIL import Image, ImageDraw, ImageTk

SWATCH_SPRITE_SIZE  = 16
SWATCH_PADDING      = 6
SWATCH_PITCH        = SWATCH_SPRITE_SIZE + SWATCH_PADDING
CURRENT_SPRITE_SIZE = 40
DEFAULT_PALETTE = []

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
        self._items        = []
        self.colors        = DEFAULT_PALETTE
        self.current_color = None
        self.current_id    = 0

        tk.Label(self.frame, text="Palette").grid(row=0, column=0)
        self.current = tk.Canvas(
            self.frame, 
            width = SWATCH_PITCH, 
            height= SWATCH_PITCH,
            highlightthickness=1
        )
        self.current.grid(row=0, column=1, padx=(0, 0))
        self.current.bind("<Button-1>",self._edit_selected_color)

        self.element = tk.Canvas(
            self.frame, 
            width = SWATCH_PITCH, 
            height= SWATCH_PITCH * 3 + SWATCH_PADDING,
            highlightthickness=0
        )
        self.element.grid(row=1, column=0, padx=(0, 8))
        self.set_colors()
        self.element.bind("<Button-1>", self._on_swatch_canvas_click)


    def _generate_sprite(self,color):
        image = Image.new("RGBA", (SWATCH_SPRITE_SIZE, SWATCH_SPRITE_SIZE), (0, 0, 0, 0))
        draw  = ImageDraw.Draw(image)
        print(color)
        draw.rectangle(xy=(0,0,SWATCH_SPRITE_SIZE,SWATCH_SPRITE_SIZE),fill=color)
        return image

    def set_colors(self,colorlist:list=None):
        if colorlist != None:
            self.colors = colorlist
                
        self.element.delete("all")
        self._sprites = []
        self._items = []
        for i, color in enumerate(self.colors):
            cx = SWATCH_PADDING
            cy = (i*SWATCH_PITCH)+SWATCH_PADDING
            sprite = ImageTk.PhotoImage(self._generate_sprite(color.color.data.toRGBHEX()))
            self._sprites.append(sprite)
            item_id = self.element.create_image(cx, cy, image=sprite)
            self._items.append((item_id, color))

        self.current_id = self._items[0][0] if self._items else None
        if len(self.colors) > 0:
            self.current_color = self.colors[0].color.data.toRGBHEX()
            self.current.config(bg=self.current_color)
            self.element.config(height=SWATCH_PITCH * len(self.colors) + SWATCH_PADDING)

    def _edit_selected_color(self, event):
        picked_color = colorchooser.askcolor(color=self.current_color, title="Choose color")[1]
        if picked_color:
            for index, (item_id, _color) in enumerate(self._items):
                if item_id == self.current_id:
                    self.current_color = picked_color.color.data.toRGBHEX()
                    self.current.config(bg=self.current_color)

                    sprite = ImageTk.PhotoImage(self._generate_sprite(picked_color))
                    self._sprites[index] = sprite
                    self.element.itemconfigure(item_id, image=sprite)
                    self._items[index] = (item_id, picked_color)
                    self.colors[index] = picked_color
                    break

    def _on_swatch_canvas_click(self, event):
        clicked = self.element.find_overlapping(event.x, event.y, event.x, event.y)
        if not clicked:
            return
        clicked_id = clicked[-1]
        for item_id, color in self._items:
            if item_id == clicked_id:
                self.current_color = color.color.data.toRGBHEX()
                self.current_id = item_id
                self.current.config(bg=self.current_color)
                
